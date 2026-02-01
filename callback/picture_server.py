from io import BytesIO
from PIL import Image
import requests
import json
from flask import Flask, request, jsonify,Response, stream_with_context
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import sys, os, uuid
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from Insights.ChatBot import __build_graph__
from libs.CeleryHelper import run_exam_task, run_eval_task
import asyncio
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage,ToolMessage
from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver
# Load environment variables from .env
load_dotenv()
from libs.Logger import logger

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "jlpt": generate_password_hash(os.getenv("FLASK_PASS"))
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users[username], password):
        return username

# Initialize Blob client
blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
container_client = blob_service_client.get_container_client(os.getenv("AZURE_IMAGE_CONTAINER", "images"))

@app.route('/4o-image-callback', methods=['POST'])
def handle_callback():
    """Handle callback from 4o image generation service."""
    data = request.json

    code = data.get('code')
    msg = data.get('msg')
    callback_data = data.get('data', {})
    task_id = callback_data.get('taskId')
    info = callback_data.get('info')

    logger.info(f"Received 4o image generation callback: taskId={task_id}, status={code}, message={msg}")

    if code == 200:
        logger.info("Task completed successfully")
        result_urls = info.get('result_urls', []) if info else []

        logger.info(f"Generated {len(result_urls)} images")
        for i, url in enumerate(result_urls):
            logger.info(f"Image {i + 1}: {url}")

            try:
                # Download image
                response = requests.get(url)
                if response.status_code == 200:
                    # Open the image
                    img = Image.open(BytesIO(response.content))

                    # Resize: long side = 500px, maintain aspect ratio
                    width, height = img.size
                    if width > height:
                        new_width = 500
                        new_height = int((500 / width) * height)
                    else:
                        new_height = 500
                        new_width = int((500 / height) * width)

                    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # Save to buffer
                    buffer = BytesIO()
                    img_resized.save(buffer, format="PNG")
                    buffer.seek(0)

                    # Blob name: organize by task
                    blob_name = f"4o_images_{task_id}_image_{i + 1}.png"

                    # Upload to Azure Blob
                    container_client.upload_blob(
                        name=blob_name,
                        data=buffer,
                        overwrite=True
                    )

                    logger.info(f"Uploaded resized {blob_name} ({new_width}x{new_height}) to Azure Blob Storage")
                else:
                    logger.error(f"Failed to download image: status {response.status_code}")

            except Exception as e:
                logger.error(f"Image download/upload failed: {e}")

    else:
        logger.error(f"4o image generation failed: {msg}")

        if code == 400:
            logger.error("Content policy violation or parameter error")
        elif code == 451:
            logger.error("Image download failed")
        elif code == 500:
            logger.error("Server internal error")

    # Always acknowledge callback
    return jsonify({'status': 'received'}), 200

@app.route("/run_exam", methods=["POST"])
@auth.login_required
def run_exam_endpoint():
    """
    Run exam job asynchronously via Celery.
    Example body:
    {
        "level": "n3",
        "exam_type": "fast_exam",
        "count": 5
    }
    """
    data = request.get_json()
    if not data or "level" not in data or "exam_type" not in data:
        return jsonify({
            "error": "Missing required parameters.",
            "required_fields": ["level", "exam_type"],
            "example": {"level": "n3", "exam_type": "fast_exam", "count": 3}
        }), 400

    level = data["level"].lower()
    exam_type = data["exam_type"].lower()
    count = int(data.get("count", 1))

    # Define valid values inside the function
    valid_levels = ["n1", "n2", "n3", "n4", "n5"]
    valid_exam_types = ["full_exam", "fast_exam", "vocab", "grammar", "reading", "listening"]

    # Validate level
    if level not in valid_levels:
        return jsonify({
            "error": f"Invalid level '{level}'.",
            "valid_levels": valid_levels,
            "hint": "Use lowercase levels: n1, n2, n3, n4, n5."
        }), 400

    # Validate exam type
    if exam_type not in valid_exam_types:
        return jsonify({
            "error": f"Invalid exam_type '{exam_type}'.",
            "valid_exam_types": valid_exam_types,
            "hint": "Use one of the supported exam types."
        }), 400

    # Validate count (1–10)
    if not (1 <= count <= 10):
        return jsonify({
            "error": f"Invalid count '{count}'.",
            "valid_range": "1–10",
            "hint": "You can queue between 1 and 10 exam runs at once."
        }), 400

    # Queue jobs
    task_ids = []
    for _ in range(count):
        # task_uuid = str(uuid.uuid1())
        task_uuid = run_exam_task.apply_async(args=(level, exam_type))
        task_ids.append(str(task_uuid))

    return jsonify({
        "status": "queued",
        "level": level,
        "exam_type": exam_type,
        "count": count,
        "task_ids": task_ids
    }), 202


@app.route("/run_eval", methods=["POST"])
@auth.login_required
def run_eval_endpoint():
    """
    Run exam job asynchronously via Celery.
    Example body:
    {
        "level": "n3",
        "exam_type": "fast_exam",
        ...
    }
    """
    data = request.get_json()

    if not data or "level" not in data or "type" not in data:
        return jsonify({
            "error": "Missing required parameters.",
            "required_fields": ["level", "type"],
            "example": {"level": "n3", "type": "fast_exam"}
        }), 400

    level = data["level"].lower()
    exam_type = data["type"].lower()

    # Define valid values inside the function
    valid_levels = ["n1", "n2", "n3", "n4", "n5"]
    valid_exam_types = ["full_exam", "fast_exam", "vocab", "grammar", "reading", "listening"]

    # Validate level
    if level not in valid_levels:
        return jsonify({
            "error": f"Invalid level '{level}'.",
            "valid_levels": valid_levels,
            "hint": "Use lowercase levels: n1, n2, n3, n4, n5."
        }), 400

    # Validate exam type
    if exam_type not in valid_exam_types:
        return jsonify({
            "error": f"Invalid exam_type '{exam_type}'.",
            "valid_exam_types": valid_exam_types,
            "hint": "Use one of the supported exam types."
        }), 400

    # create a job
    task_uuid = run_eval_task.apply_async(args=[json.dumps(data, ensure_ascii=False)])

    return jsonify({
        "status": "queued",
        "level": level,
        "type": exam_type,
        "task_id": str(task_uuid)
    }), 202


@app.route("/status/<task_id>", methods=["GET"])
@auth.login_required
def get_status(task_id):
    """
    Get detailed state info of a Celery job by ID.
    """
    task = run_exam_task.AsyncResult(task_id)

    response = {"task_id": task.id, "state": task.state}

    if task.state == "PENDING":
        response["message"] = "Task is waiting in the queue or not yet started."

    elif task.state == "RECEIVED":
        response["message"] = "Task has been received by a worker."

    elif task.state == "STARTED":
        response["message"] = "Task is currently running."

    elif task.state == "RETRY":
        response["message"] = "Task is being retried after a failure."
        response["error"] = str(task.info)

    elif task.state == "FAILURE":
        response["message"] = "Task failed during execution."
        response["error"] = str(task.info)

    elif task.state == "SUCCESS":
        response["message"] = "Task completed successfully."

    elif task.state == "PROGRESS":
        # if you use update_state() with meta info
        response["message"] = "Task is in progress."
        response["meta"] = task.info

    else:
        response["message"] = "Unknown state."

    return jsonify(response), 200

# 3️⃣ SSE streaming endpoint

mongoClient =  MongoClient(os.getenv("AZURE_MONGO_CONNECTION"))

checkpointer = MongoDBSaver(
    mongoClient,  # MongoDB client
    db_name="memories",  # Database name
    collection_name="thread_checkpoints",  # Collection for conversation state
    ttl=86400 * 7
)

teacher_graph = __build_graph__(checkpointer)


@app.route("/chat", methods=["POST"])
@auth.login_required
def chat():
    """Stream chat responses with optional level and question_type."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate required field
        if "messages" not in data:
            return jsonify({"error": "Missing required field: messages"}), 400

        # Extract data with defaults
        user_input = data["messages"]
        level = data.get("level", "N3")  # Default to N3 if not provided
        question_type = data.get("question_type", "vocabulary")  # Default to vocabulary
        route = data.get("router","word")
        thread_id = data.get("thread_id", f"user-{uuid.uuid4().hex[:8]}")  # Generate unique ID if not provided

        # Validate data types
        if not isinstance(user_input, list):
            return jsonify({"error": "messages must be a list"}), 400

        # Validate each message in the list
        for i, msg in enumerate(user_input):
            if not isinstance(msg, dict):
                return jsonify({"error": f"Message at index {i} must be an object"}), 400
            if "role" not in msg or "content" not in msg:
                return jsonify({"error": f"Message at index {i} must have 'role' and 'content' fields"}), 400

        # Validate level if provided
        valid_levels = ["n1", "n2", "n3", "n4", "n5"]
        if level not in valid_levels:
            return jsonify({
                "error": f"Invalid level: {level}. Must be one of: {', '.join(valid_levels)}"
            }), 400

        config = {"configurable": {"thread_id": thread_id}}

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        return jsonify({"error": f"Invalid request data: {str(e)}"}), 400

    def generate():
        """Generate SSE events from the teacher graph."""
        loop = None
        try:
            # Create and set event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Prepare input data with defaults
            input_data = {
                "level": level,
                "question_type": question_type,
                "messages": user_input,
                "route": route
            }

            # Optional: Log the request for debugging (remove in production)
            logger.info(f"Processing chat request: level={level}, question_type={question_type}, "
                  f"thread_id={thread_id}, messages_count={len(user_input)}")

            async def stream_events():
                """Async generator for processing graph events."""
                try:
                    async for event in teacher_graph.astream_events(
                            input_data,
                            config,
                            stream_mode="updates",
                            version="v1"
                    ):
                        event_type = event.get("event", "")

                        # Handle chat model streaming
                        if (event_type == "on_chat_model_stream" and
                                event.get("metadata", {}).get("langgraph_node") in ["jlpt_question_explain_node", "jlpt_word_explain_node"]):

                            chunk_data = event.get("data", {})
                            if "chunk" in chunk_data and hasattr(chunk_data["chunk"], "content"):
                                content = chunk_data["chunk"].content

                                if content and isinstance(content, list):
                                    for item in content:
                                        if (isinstance(item, dict) and
                                                item.get("type") == "text" and
                                                "text" in item):
                                            text = item["text"].strip()
                                            if text:
                                                yield json.dumps({
                                                    "type": "text",
                                                    "content": text
                                                }, ensure_ascii=False)

                        # Handle follow-up questions
                        elif (event_type == "on_chain_end" and
                              event.get("name") == "suggested_question_node"):

                            output = event.get("data", {}).get("output", {})
                            if isinstance(output, dict) and "questions" in output:
                                questions_obj = output["questions"]
                                if hasattr(questions_obj, "questions"):
                                    question_list = questions_obj.questions
                                    if isinstance(question_list, list) and question_list:
                                        yield json.dumps({
                                            "type": "follow-ups",
                                            "content": question_list,
                                        }, ensure_ascii=False)

                except Exception as e:
                    logger.error(f"Error in stream_events: {e}")
                    yield json.dumps({
                        "type": "error",
                        "content": "Streaming error occurred",
                        "metadata": {"error": str(e)}
                    }, ensure_ascii=False)

            # Process async generator
            async_gen = stream_events()
            while True:
                try:
                    chunk = loop.run_until_complete(async_gen.__anext__())
                    yield f"data: {chunk}\n\n"
                except StopAsyncIteration:
                    # Send completion signal
                    yield f"data: {json.dumps({
                        'type': 'complete',
                        'content': '',
                        'metadata': {
                            'level': level,
                            'question_type': question_type,
                            'thread_id': thread_id
                        }
                    }, ensure_ascii=False)}\n\n"
                    break
                except asyncio.CancelledError:
                    # Handle client disconnection
                    logger.error(f"Client disconnected for thread_id: {thread_id}")
                    break
                except Exception as e:
                    logger.error(f"Error processing chunk: {e}")
                    yield f"data: {json.dumps({
                        'type': 'error',
                        'content': 'Failed to process response',
                        'metadata': {'error': str(e)}
                    }, ensure_ascii=False)}\n\n"
                    break

        except Exception as e:
            # Log the error for debugging
            logger.error(f"Error in chat stream: {str(e)}")
            import traceback
            traceback.print_exc()

            yield f"data: {json.dumps({
                'type': 'error',
                'content': 'Internal server error'
            }, ensure_ascii=False)}\n\n"
        finally:
            if loop and not loop.is_closed():
                loop.close()
                logger.info(f"Cleaned up event loop for thread_id: {thread_id}")

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no',
            'Access-Control-Allow-Origin': '*',
            'Content-Encoding': 'identity'
        }
    )


@app.route("/chat_history", methods=["POST"])
@auth.login_required
def chat_history():
    try:
        # 检查请求是否有JSON数据
        if request.json is None:
            return jsonify({"error": "请求必须包含JSON数据"}), 400

        data = request.json

        # 检查thread_id是否存在，如果没有则使用默认值
        thread_id = data.get("thread_id", "default-user")

        # 尝试获取聊天状态
        try:
            result = teacher_graph.get_state(
                config={
                    "configurable": {
                        "thread_id": thread_id
                    }
                }
            )
        except Exception as e:
            return jsonify({"error": f"获取聊天历史失败: {str(e)}"}), 404

        # 检查result中是否有messages字段
        if not hasattr(result, 'values') or not hasattr(result.values, '__getitem__'):
            return jsonify({"error": "返回的数据格式不正确"}), 500

        messages = result.values.get("messages", [])

        chat_history = []

        for msg in messages:
            try:
                # 确定消息角色
                if isinstance(msg, HumanMessage):
                    role = "user"
                elif isinstance(msg, AIMessage):
                    role = "assistant"
                elif isinstance(msg, SystemMessage):
                    role = "system"
                elif isinstance(msg, ToolMessage):
                    role = "tool"
                else:
                    # 尝试获取消息类型，如果失败则使用默认值
                    try:
                        role = msg.type
                    except AttributeError:
                        role = "unknown"

                # 提取消息内容
                try:
                    if isinstance(msg.content, list):
                        text = "".join(
                            part.get("text", "")
                            for part in msg.content
                            if isinstance(part, dict)
                        )
                    else:
                        text = msg.content
                except AttributeError:
                    text = ""

                chat_history.insert(0, {
                    "role": role,
                    "content": text
                })

            except Exception as msg_error:
                # 跳过处理失败的单条消息，继续处理其他消息
                continue

        return jsonify({"chat_history": chat_history})

    except Exception as e:
        # 捕获所有未处理的异常
        return jsonify({"error": f"服务器内部错误: {e}"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)

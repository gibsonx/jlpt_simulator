from io import BytesIO
from PIL import Image
import requests
from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import sys, os,uuid
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from libs.CeleryHelper import run_exam_task
# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

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

    print(f"Received 4o image generation callback: taskId={task_id}, status={code}, message={msg}")

    if code == 200:
        print("Task completed successfully")
        result_urls = info.get('result_urls', []) if info else []

        print(f"Generated {len(result_urls)} images")
        for i, url in enumerate(result_urls):
            print(f"Image {i + 1}: {url}")

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

                    print(f"Uploaded resized {blob_name} ({new_width}x{new_height}) to Azure Blob Storage")
                else:
                    print(f"Failed to download image: status {response.status_code}")

            except Exception as e:
                print(f"Image download/upload failed: {e}")

    else:
        print(f"4o image generation failed: {msg}")

        if code == 400:
            print("Content policy violation or parameter error")
        elif code == 451:
            print("Image download failed")
        elif code == 500:
            print("Server internal error")

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
        task_uuid = str(uuid.uuid1())
        run_exam_task.delay(level, exam_type, task_uuid)
        task_ids.append(task_uuid)

    return jsonify({
        "status": "queued",
        "level": level,
        "exam_type": exam_type,
        "count": count,
        "task_ids": task_ids
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)

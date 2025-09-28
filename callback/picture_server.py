import os
import requests
from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from libs.CeleryHelper import run_exam_task


# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

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
                    # Blob name: organize by task
                    blob_name = f"4o_images_{task_id}_image_{i + 1}.png"

                    # Upload to Azure Blob
                    container_client.upload_blob(
                        name=blob_name,
                        data=response.content,
                        overwrite=True
                    )

                    print(f"Uploaded {blob_name} to Azure Blob Storage")
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
def run_exam_endpoint():
    """
    Run exam job asynchronously via Celery.
    Body example: { "level": "N3", "exam_type": "fast_exam", "count": 5 }
    """
    data = request.get_json()
    if not data or "level" not in data or "exam_type" not in data:
        return jsonify({"error": "Missing 'level' or 'exam_type'"}), 400

    level = data["level"]
    exam_type = data["exam_type"]
    count = data.get("count", 1)  # run how many times

    # Queue multiple jobs
    task_ids = []
    for _ in range(count):
        task = run_exam_task.delay(level, exam_type)
        task_ids.append(task.id)

    return jsonify({"status": "queued", "task_ids": task_ids}), 202


@app.route("/status/<task_id>", methods=["GET"])
def get_status(task_id):
    """
    Get status and result of a Celery job by ID.
    """
    task = run_exam_task.AsyncResult(task_id)
    if task.state == "PENDING":
        return jsonify({"state": task.state, "result": None}), 200
    elif task.state == "FAILURE":
        return jsonify({"state": task.state, "error": str(task.info)}), 500
    else:
        return jsonify({"state": task.state, "result": task.result}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
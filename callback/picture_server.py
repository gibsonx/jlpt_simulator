import os
import requests
from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
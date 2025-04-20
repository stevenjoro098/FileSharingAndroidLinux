import shared_state
from flask import Flask, request
import queue

from notifier import show_notification

app = Flask(__name__)
message_queue = queue.Queue()
@app.route('/')
def index():
    return 'LinkBridge Server is Running'

from flask import request, jsonify
import os
from werkzeug.utils import secure_filename
from notifier import show_notification
import shared_state

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/share', methods=['POST'])
def share():
    try:
        # Handle file upload
        uploaded_file = request.files.get('file')
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(filepath)

            message = f"📁 Received file: {filename}"
            shared_state.update_message(message)
            shared_state.message_queue.put(message)
            show_notification("LinkBridge", message)

            return jsonify({
                "status": "success",
                "type": "file",
                "filename": filename
            }), 200

        # Handle text or link data
        content = request.form.get('content') or (request.json.get('content') if request.is_json else None)
        if content:
            message = f"📝 Received content: {content[:60]}{'...' if len(content) > 60 else ''}"
            shared_state.update_message(message)
            shared_state.message_queue.put(message)
            show_notification("LinkBridge", message)

            return jsonify({
                "status": "success",
                "type": "text",
                "content": content
            }), 200

        # No valid data provided
        return jsonify({
            "status": "error",
            "message": "No valid file or content received."
        }), 400

    except Exception as e:
        error_msg = f"⚠️ Error: {str(e)}"
        shared_state.update_message(error_msg)
        shared_state.message_queue.put(error_msg)
        show_notification("LinkBridge", error_msg)
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred.",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
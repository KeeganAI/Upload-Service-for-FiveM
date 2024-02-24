from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

app = Flask(__name__)

BASE_UPLOAD_FOLDER = 'C:\\Users\\Keeg\\Desktop\\pyTest\\uploads'
SAVE_REQUEST_DETAILS = True  

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'webm', 'avi', 'png', 'jpg', 'jpeg', 'gif', 'flac', 'webp'}
API_KEYS = {
    'Video': "D&zE#MyK5GSoB@@&gA!G84etXazdxbLDCrkTHqyH",
    'Image': "$Eycm3gg$EDm&S6aY?4FeJHoF#4YpTJ4x4LNq73E",
    'Audio': "Q&pJmApo?gBPYAkyENCijF5mPc&z4T&gAtF7E38#",
}
FOLDERS = {
    'mp3': 'Audio', 'wav': 'Audio', 'mp4': 'Video', 'webm': 'Video', 'avi': 'Video',
    'png': 'Image', 'jpg': 'Image', 'jpeg': 'Image', 'gif': 'Image', 'flac': 'Audio', 'webp': 'Image',
}

def allowed_file(filename):
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_api_key(headers, file_type):
    api_key = headers.get('Authorization')
    return api_key and API_KEYS.get(file_type) == api_key

def save_request_details_if_enabled(request, additional_info=None):
    if not SAVE_REQUEST_DETAILS:
        return
    
    file_path = os.path.join(BASE_UPLOAD_FOLDER, 'request_details.json')
    request_info = {
        'headers': dict(request.headers),
        'args': request.args.to_dict(),
        'form': request.form.to_dict(),
        'json': request.get_json(silent=True),
        **(additional_info or {})
    }

    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r+') as file:
                file_data = json.load(file)
                file_data.append(request_info)
                file.seek(0)
                file.truncate()
                json.dump(file_data, file, indent=4)
        else:
            with open(file_path, 'w') as file:
                json.dump([request_info], file, indent=4)
    except json.JSONDecodeError:
        with open(file_path, 'w') as file:
            json.dump([request_info], file, indent=4)

@app.route('/upload', methods=['POST'])
def upload_file():
    save_request_details_if_enabled(request)
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'status': 400, 'data': {'error': 'No file part'}}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'status': 400, 'data': {'error': 'No selected file'}}), 400
    
    extension = file.filename.rsplit('.', 1)[1].lower()
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'status': 400, 'data': {'error': 'File not allowed'}}), 400

    file_type = FOLDERS.get(extension)
    if not file_type or not check_api_key(request.headers, file_type):
        return jsonify({'success': False, 'status': 403, 'data': {'error': 'Invalid API key or file type'}}), 403

    upload_folder = os.path.join(BASE_UPLOAD_FOLDER, file_type)
    os.makedirs(upload_folder, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{secure_filename(file.filename.rsplit('.', 1)[0])}_{timestamp}.{extension}"
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    save_request_details_if_enabled(request, {'file_saved': filename, 'status': 'success'})

    return jsonify({'success': True, 'status': 200, 'data': {'url': f'http://{request.host}/uploads/{file_type}/{filename}'}}), 200

@app.route('/uploads/<file_type>/<filename>')
def uploaded_file(file_type, filename):
    return send_from_directory(os.path.join(BASE_UPLOAD_FOLDER, file_type), filename)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

app = Flask(__name__)

BASE_UPLOAD_FOLDER = 'D:\\xampp\\htdocs\\uploads'
FILE_ACCESS_URL = 'http://localhost/uploads'

SAVE_REQUEST_DETAILS = True

ALLOWED_EXTENSIONS = {'ogg', 'mp4', 'webp'}

API_KEYS = {
    'Video': "INSERT_A_NEW_API_KEY_HERE",
    'Image': "INSERT_A_NEW_API_KEY_HERE",
    'Audio': "INSERT_A_NEW_API_KEY_HERE",
}
FOLDERS = {
    'ogg': 'Audio', 'mp3': 'Audio', 
    'mp4': 'Video', 'webm': 'Video',
    'png': 'Image', 'gif': 'Image', 'webp': 'Image',
}

def allowed_file(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    print(f"file extension received: .{extension}")
    return extension in ALLOWED_EXTENSIONS

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
        return jsonify({'success': False, 'status': 400, 'data': {'error': 'No file'}}), 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'success': False, 'status': 400, 'data': {'error': 'No file or file not allowed'}}), 400
    
    extension = file.filename.rsplit('.', 1)[1].lower()
    file_type = FOLDERS.get(extension)
    if not check_api_key(request.headers, file_type):
        response_data = {'success': False, 'status': 403, 'data': {'error': 'Invalid API key or file type'}}
        print(json.dumps(response_data, indent=4))
        return jsonify(response_data), 403

    upload_folder = os.path.join(BASE_UPLOAD_FOLDER, file_type)
    os.makedirs(upload_folder, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{secure_filename(file.filename.rsplit('.', 1)[0])}_{timestamp}.{extension}"
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    file_url = f'{FILE_ACCESS_URL}/{file_type}/{filename}'

    response = {'success': True, 'status': 200, 'url': file_url}
    return jsonify(response), 200

@app.route('/uploads/<file_type>/<filename>')
def uploaded_file(file_type, filename):
    directory = os.path.join(BASE_UPLOAD_FOLDER, file_type)
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(debug=True)

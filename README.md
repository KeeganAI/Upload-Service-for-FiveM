# Flask Upload Service for FiveM

## Overview
This Flask application provides a specialized upload service initially designed for the "lb-phone" resource in FiveM. It's engineered to overcome the limitations often encountered with Discord webhooks, especially regarding file handling such as availability issues, rate limiting, and file size restrictions. While similar services are commercially available, this solution offers a cost-effective and self-hosted alternative, promising future enhancements including a possible web management panel.

## Features
- **API Key Authentication**: Secure file uploads with distinct API keys for audio, video, and image files.
- **Organized File Storage**: Automatically sorts uploaded files into respective folders based on their type.
- **Unique Filenames**: Appends a timestamp to filenames to ensure uniqueness and prevent overwrites.
- **Request Detail Logging**: Optional logging of request details for audit and debug purposes.
- **Versatile Use**: Although initially created for FiveM's "lb-phone" resource, its utility extends to various other applications.

## Getting Started

### Prerequisites
- Python 3.x
- Flask

### Installation
1. Ensure Python 3.x and pip are installed on your system.
2. Install Flask using pip:

## Usage

```python
pip install Flask

```

### Configuration
1. Modify `API_KEYS` in the script to your desired API keys for video, image, and audio uploads.
2. Set `BASE_UPLOAD_FOLDER` to your preferred upload directory path.

### Running the Server
Launch the server by running:

```python
python app.py
```
This starts the Flask server, making it listen for upload requests on `/upload`.

### Uploading Files
To upload a file, send a POST request to `http://<server-address>:5000/upload` with the file and the correct `Authorization` header corresponding to the file type.

## Future Plans
- **Web Management Panel**: Considering the addition of a user-friendly interface for managing uploaded files and configurations.
- **Enhanced File Support**: Open to expanding support for more file types and features based on user feedback.

## Note
This project was developed with the "lb-phone" resource for FiveM in mind but is versatile enough for other uses. It aims to bypass long-term limitations of Discord webhooks and avoid the costs associated with similar hosted services, even though it currently does not offer a web panel (potentially in the future).

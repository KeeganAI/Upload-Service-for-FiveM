# Flask Upload Service for FiveM

## Overview
This application offers a simplified upload service tailored to the "lb-phone" resource in FiveM. 
It addresses common issues faced while integrating with Discord Webhooks, such as file availability, rate limits or paid services...

## Features
- **API Key Authentication**: Enhances security by requiring distinct API keys for audio, video, and image files, ensuring that file uploads are authenticated and authorized.
- **Organized File Storage**: Maintains a structured storage system by automatically sorting uploaded files into respective folders based on their type, facilitating easy management and access.
- **Unique Filenames**: To prevent file overwrites and ensure that each uploaded file can be uniquely identified, the service appends a timestamp to the original filenames.
- **Comprehensive URL Access**: Returns the complete URL of the uploaded file, including its original extension, allowing for straightforward integration and access within applications.
- **Request Detail Logging**: Offers an optional feature to log the details of each upload request, including headers and file information, which is invaluable for auditing, debugging, and monitoring upload activity.
- **Simplified File Handling**: By directly storing and serving files in their original formats without unnecessary conversions, the service streamlines the upload process, ensuring efficiency and reliability.
- **Future-Ready**: Open to further enhancements, including the potential development of a web management interface and the addition of support for more file types, based on community feedback and evolving requirements.

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
1. Set `BASE_UPLOAD_FOLDER` to your preferred upload directory path.
2. Adjust `FILE_ACCESS_URL` to match your server's address for accessing the uploaded files.
3. Setup the `url` in `lb-phone\shared\upload.lua`, which should be lines 10, 25 and 40
4. Remove the `suffix` lines in `lb-phone\shared\upload.lua`, which should be lines 22, 37 and 52
5. Create a new "api key" (you can type whatever you want), just make sure to use the same "per-type", 

```python
# app.py
API_KEYS = {
    'Video': "blabla1",
    'Image': "blabla2",
    'Audio': "blabla3",
}
```
```lua
-- lb-phone\server\apiKeys.lua
API_KEYS = {
    Video = "blabla1",
    Image = "blabla2",
    Audio = "blabla3",
}
```

### Running the Server
Launch the .py file by running:

```python
python app.py
```
The server will then listen for upload requests at /upload.

### Uploading Files
Just try to shot a photo, make a video or record a memo.

## Future Plans
- **Web Panel**: Considering the addition of a user-friendly interface for managing uploaded files.

## Note
This project was developed with the "lb-phone" resource for FiveM in mind but is versatile enough for other uses. 
It aims to bypass the long-term limitations of Discord webhooks and avoid the costs associated with similar "cloud" services, even though it currently does not offer a web panel (potentially in the future).

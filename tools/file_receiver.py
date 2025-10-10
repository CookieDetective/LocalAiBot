import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploaded_files"
ALLOWED_EXTENSIONS = {"xlsx", "json", "csv", "txt"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def receive_file(file_storage):
    """Receives a file from Flask's request.files and saves it."""
    if not allowed_file(file_storage.filename):
        raise ValueError("File type not allowed.")
    filename = secure_filename(file_storage.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_storage.save(save_path)
    return save_path  # Return path for further processing
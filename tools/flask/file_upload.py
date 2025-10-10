from flask import Blueprint, request, jsonify
from tools.file_receiver import receive_file

bp = Blueprint('file_upload', __name__)

@bp.route('/upload', methods=['POST'])
def upload():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400
    try:
        file_path = receive_file(file)
        return jsonify({"message": f"File uploaded: {file_path}"})
    except Exception as e:
        return jsonify({"message": str(e)}), 400
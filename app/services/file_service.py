import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}

MAX_FILE_SIZE = 10 * 1024 * 1024

os.makedirs(UPLOAD_DIR, exist_ok=True)


def validate_file(file: UploadFile):

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type")

    return extension


async def save_file(file: UploadFile):

    extension = validate_file(file)

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise ValueError("Maximum file size is 10 MB")

    unique_name = f"{uuid.uuid4()}{extension}"

    path = os.path.join(UPLOAD_DIR, unique_name)

    with open(path, "wb") as f:
        f.write(contents)

    return {
        "filename": unique_name,
        "filepath": path,
        "extension": extension,
        "filesize": len(contents)
    }
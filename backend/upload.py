"""FastAPI application for a private S3 photo gallery."""

import mimetypes
import os
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import RedirectResponse

from .delete_photo import delete_photo
from .photos import album_prefix, create_download_url, get_s3_client, list_photos, require_bucket

app = FastAPI(title="Cloud Photo Gallery")
MAX_UPLOAD_BYTES = int(os.environ.get("MAX_UPLOAD_BYTES", 10 * 1024 * 1024))
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/photos", status_code=201)
async def upload_photo(album: str = Form(...), photo: UploadFile = File(...)):
    if photo.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Only JPEG, PNG, WebP, and GIF images are supported")
    content = await photo.read(MAX_UPLOAD_BYTES + 1)
    if not content or len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail=f"Photo must be between 1 byte and {MAX_UPLOAD_BYTES} bytes")

    suffix = Path(photo.filename or "photo").suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        suffix = mimetypes.guess_extension(photo.content_type) or ".jpg"
    key = f"{album_prefix(album)}{uuid4().hex}{suffix}"
    get_s3_client().put_object(
        Bucket=require_bucket(), Key=key, Body=content, ContentType=photo.content_type
    )
    return {"key": key, "album": album, "filename": photo.filename}


@app.get("/photos")
def get_photos(album: str | None = None):
    return {"photos": list_photos(album)}


@app.get("/photos/{key:path}/download")
def download_photo(key: str):
    try:
        return RedirectResponse(create_download_url(key))
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.delete("/photos/{key:path}", status_code=204)
def remove_photo(key: str):
    delete_photo(key)

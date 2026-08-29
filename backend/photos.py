"""S3-backed photo listing and organization helpers."""

import os
import re

import boto3


BUCKET_NAME = os.environ.get("PHOTO_BUCKET_NAME", "")
ALBUM_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _-]{0,63}$")


def get_s3_client():
    return boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-east-1"))


def require_bucket() -> str:
    if not BUCKET_NAME:
        raise RuntimeError("PHOTO_BUCKET_NAME must be configured")
    return BUCKET_NAME


def validate_album(album: str) -> str:
    if not ALBUM_PATTERN.fullmatch(album):
        raise ValueError("Album names may contain letters, numbers, spaces, hyphens, and underscores")
    return album


def album_prefix(album: str | None = None) -> str:
    return f"albums/{validate_album(album)}/" if album else "albums/"


def list_photos(album: str | None = None) -> list[dict]:
    """Return photo metadata without exposing public S3 URLs."""
    response = get_s3_client().list_objects_v2(Bucket=require_bucket(), Prefix=album_prefix(album))
    photos = []
    for item in response.get("Contents", []):
        if item["Key"].endswith("/"):
            continue
        photos.append(
            {
                "key": item["Key"],
                "filename": item["Key"].rsplit("/", 1)[-1],
                "album": item["Key"].split("/")[1],
                "size": item["Size"],
                "last_modified": item["LastModified"].isoformat(),
            }
        )
    return photos


def create_download_url(key: str, expires_in: int = 900) -> str:
    """Create a short-lived private download URL for a stored photo."""
    if not key.startswith("albums/"):
        raise ValueError("Invalid photo key")
    return get_s3_client().generate_presigned_url(
        "get_object", Params={"Bucket": require_bucket(), "Key": key}, ExpiresIn=expires_in
    )

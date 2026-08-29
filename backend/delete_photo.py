"""Photo deletion route."""

from fastapi import HTTPException

from .photos import get_s3_client, require_bucket


def delete_photo(key: str) -> None:
    if not key.startswith("albums/"):
        raise HTTPException(status_code=400, detail="Invalid photo key")
    get_s3_client().delete_object(Bucket=require_bucket(), Key=key)

"""Lambda handler that creates a private S3 upload URL and metadata record."""

import os
from datetime import UTC, datetime
from uuid import uuid4

from .lambda_utils import (
    ALLOWED_CONTENT_TYPES,
    json_response,
    metadata_table,
    optional_text,
    photos_bucket_name,
    request_body,
    required_text,
    s3_client,
    safe_file_name,
    safe_identifier,
)


def lambda_handler(event, _context):
    try:
        payload = request_body(event)
        user_id = safe_identifier(required_text(payload, "userId", 100), "userId")
        file_name = safe_file_name(required_text(payload, "fileName", 255))
        content_type = required_text(payload, "contentType", 100).lower()
        if content_type not in ALLOWED_CONTENT_TYPES:
            return json_response(415, {"message": "Unsupported image type"})

        photo_id = str(uuid4())
        created_at = datetime.now(UTC).isoformat()
        s3_key = f"users/{user_id}/photos/{photo_id}/{file_name}"
        metadata = {
            "photoId": photo_id,
            "userId": user_id,
            "fileName": file_name,
            "title": optional_text(payload, "title", 160),
            "description": optional_text(payload, "description", 2000),
            "category": optional_text(payload, "category", 80),
            "tags": payload.get("tags", []),
            "s3Key": s3_key,
            "createdAt": created_at,
            "uploadStatus": "PENDING",
        }
        if not isinstance(metadata["tags"], list) or not all(isinstance(tag, str) for tag in metadata["tags"]):
            raise ValueError("tags must be an array of text values")

        metadata_table().put_item(Item=metadata)
        expires_in = int(os.environ.get("UPLOAD_URL_EXPIRY_SECONDS", "900"))
        upload_url = s3_client().generate_presigned_url(
            "put_object",
            Params={"Bucket": photos_bucket_name(), "Key": s3_key, "ContentType": content_type},
            ExpiresIn=expires_in,
            HttpMethod="PUT",
        )
        return json_response(
            201,
            {
                "photoId": photo_id,
                "uploadUrl": upload_url,
                "method": "PUT",
                "headers": {"Content-Type": content_type},
                "expiresIn": expires_in,
            },
        )
    except (ValueError, KeyError) as error:
        return json_response(400, {"message": str(error)})

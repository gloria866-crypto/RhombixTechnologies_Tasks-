"""Photo deletion helpers and the Step 5 Lambda handler."""

from botocore.exceptions import ClientError

from fastapi import HTTPException

from .lambda_utils import cors_headers, json_response, metadata_table, photos_bucket_name, safe_identifier, s3_client
from .photos import get_s3_client, require_bucket


def delete_photo(key: str) -> None:
    if not key.startswith("albums/"):
        raise HTTPException(status_code=400, detail="Invalid photo key")
    get_s3_client().delete_object(Bucket=require_bucket(), Key=key)


def lambda_handler(event, _context):
    """Delete one user's S3 object and its DynamoDB metadata."""
    photo_id = (event.get("pathParameters") or {}).get("id", "").strip()
    parameters = event.get("queryStringParameters") or {}
    try:
        photo_id = safe_identifier(photo_id, "photo id")
        user_id = safe_identifier(parameters.get("userId", "").strip(), "userId")
    except ValueError as error:
        return json_response(400, {"message": str(error)})

    try:
        item = metadata_table().get_item(Key={"photoId": photo_id}).get("Item")
        if not item:
            return json_response(404, {"message": "Photo not found"})
        if item["userId"] != user_id:
            return json_response(403, {"message": "You cannot delete this photo"})

        s3_client().delete_object(Bucket=photos_bucket_name(), Key=item["s3Key"])
        metadata_table().delete_item(Key={"photoId": photo_id})
        return {"statusCode": 204, "headers": cors_headers(), "body": ""}
    except (KeyError, ClientError):
        return json_response(500, {"message": "Unable to delete the photo"})

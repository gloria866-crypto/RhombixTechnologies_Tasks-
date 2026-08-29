"""Lambda handler that retrieves a user's photo metadata."""

from boto3.dynamodb.conditions import Key

from .lambda_utils import json_response, metadata_table, safe_identifier


def lambda_handler(event, _context):
    parameters = event.get("queryStringParameters") or {}
    try:
        user_id = safe_identifier(parameters.get("userId", "").strip(), "userId")
    except ValueError as error:
        return json_response(400, {"message": str(error)})

    try:
        limit = min(max(int(parameters.get("limit", 20)), 1), 100)
    except ValueError:
        return json_response(400, {"message": "limit must be a number"})

    response = metadata_table().query(
        IndexName="UserPhotosIndex",
        KeyConditionExpression=Key("userId").eq(user_id),
        Limit=limit,
        ScanIndexForward=False,
    )
    return json_response(200, {"photos": response.get("Items", [])})

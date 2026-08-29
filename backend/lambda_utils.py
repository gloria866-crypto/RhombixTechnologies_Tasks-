"""Shared helpers for the photo-gallery Lambda handlers."""

import json
import os
import re

import boto3


ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
SAFE_FILE_NAME = re.compile(r"[^A-Za-z0-9._-]")
SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9_-]{1,100}$")


def s3_client():
    return boto3.client("s3")


def metadata_table():
    return boto3.resource("dynamodb").Table(os.environ["PHOTO_METADATA_TABLE_NAME"])


def photos_bucket_name() -> str:
    return os.environ["PHOTOS_BUCKET_NAME"]


def json_response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN", "http://localhost:3000"),
        },
        "body": json.dumps(body, default=str),
    }


def cors_headers() -> dict:
    return {"Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN", "http://localhost:3000")}


def request_body(event: dict) -> dict:
    body = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        raise ValueError("Base64 request bodies are not supported")
    parsed = json.loads(body) if isinstance(body, str) else body
    if not isinstance(parsed, dict):
        raise ValueError("Request body must be a JSON object")
    return parsed


def required_text(payload: dict, field: str, max_length: int = 250) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip() or len(value.strip()) > max_length:
        raise ValueError(f"{field} is required and must be at most {max_length} characters")
    return value.strip()


def optional_text(payload: dict, field: str, max_length: int = 1000) -> str:
    value = payload.get(field, "")
    if not isinstance(value, str) or len(value.strip()) > max_length:
        raise ValueError(f"{field} must be text and at most {max_length} characters")
    return value.strip()


def safe_file_name(file_name: str) -> str:
    cleaned = SAFE_FILE_NAME.sub("-", file_name.rsplit("/", 1)[-1]).strip(".-")
    if not cleaned:
        raise ValueError("fileName is invalid")
    return cleaned


def safe_identifier(value: str, field: str) -> str:
    if not isinstance(value, str) or not SAFE_IDENTIFIER.fullmatch(value):
        raise ValueError(f"{field} may only contain letters, numbers, hyphens, and underscores")
    return value

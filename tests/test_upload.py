import os

import boto3
import pytest
from moto import mock_aws

os.environ["PHOTO_BUCKET_NAME"] = "test-photo-gallery"

from backend import photos


@pytest.fixture(autouse=True)
def s3_bucket(monkeypatch):
    monkeypatch.setattr(photos, "BUCKET_NAME", "test-photo-gallery")
    with mock_aws():
        client = boto3.client("s3", region_name="us-east-1")
        client.create_bucket(Bucket="test-photo-gallery")
        yield client


def test_photo_upload_is_stored_privately(s3_bucket):
    key = "albums/Holidays/photo.jpg"
    s3_bucket.put_object(Bucket="test-photo-gallery", Key=key, Body=b"image-data", ContentType="image/jpeg")

    stored = s3_bucket.get_object(Bucket="test-photo-gallery", Key=key)
    assert stored["ContentType"] == "image/jpeg"
    assert stored["Body"].read() == b"image-data"

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
        client.put_object(Bucket="test-photo-gallery", Key="albums/Travel/beach.jpg", Body=b"x")
        client.put_object(Bucket="test-photo-gallery", Key="albums/Work/diagram.png", Body=b"y")
        yield


def test_list_photos_filters_by_album():
    result = photos.list_photos("Travel")
    assert len(result) == 1
    assert result[0]["filename"] == "beach.jpg"
    assert result[0]["album"] == "Travel"


def test_album_names_reject_path_traversal():
    with pytest.raises(ValueError):
        photos.album_prefix("../private")

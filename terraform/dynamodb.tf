# Step 4: metadata is stored separately from image files in S3.
resource "aws_dynamodb_table" "photo_metadata" {
  name         = var.photo_metadata_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "photoId"

  attribute {
    name = "photoId"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    Application = "cloud-photo-gallery"
    Purpose     = "photo-metadata"
  }
}

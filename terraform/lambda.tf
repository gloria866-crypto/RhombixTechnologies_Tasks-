# Step 5: package only the Lambda code and its shared Python helpers.
data "archive_file" "photo_lambdas" {
  type        = "zip"
  output_path = "${path.module}/.build/photo-lambdas.zip"

  source {
    content  = file("${path.module}/../backend/__init__.py")
    filename = "backend/__init__.py"
  }
  source {
    content  = file("${path.module}/../backend/lambda_utils.py")
    filename = "backend/lambda_utils.py"
  }
  source {
    content  = file("${path.module}/../backend/photos.py")
    filename = "backend/photos.py"
  }
  source {
    content  = file("${path.module}/../backend/generate_upload_url.py")
    filename = "backend/generate_upload_url.py"
  }
  source {
    content  = file("${path.module}/../backend/get_photos.py")
    filename = "backend/get_photos.py"
  }
  source {
    content  = file("${path.module}/../backend/delete_photo.py")
    filename = "backend/delete_photo.py"
  }
}

locals {
  lambda_environment = {
    PHOTOS_BUCKET_NAME        = aws_s3_bucket.photos.bucket
    PHOTO_METADATA_TABLE_NAME = aws_dynamodb_table.photo_metadata.name
    ALLOWED_ORIGIN            = "http://localhost:3000"
    UPLOAD_URL_EXPIRY_SECONDS = "900"
  }
}

resource "aws_lambda_function" "generate_upload_url" {
  function_name    = "cloud-photo-gallery-generate-upload-url"
  role             = aws_iam_role.photo_lambda.arn
  handler          = "backend.generate_upload_url.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.photo_lambdas.output_path
  source_code_hash = data.archive_file.photo_lambdas.output_base64sha256
  timeout          = 15

  environment { variables = local.lambda_environment }
}

resource "aws_lambda_function" "get_photos" {
  function_name    = "cloud-photo-gallery-get-photos"
  role             = aws_iam_role.photo_lambda.arn
  handler          = "backend.get_photos.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.photo_lambdas.output_path
  source_code_hash = data.archive_file.photo_lambdas.output_base64sha256
  timeout          = 15

  environment { variables = local.lambda_environment }
}

resource "aws_lambda_function" "delete_photo" {
  function_name    = "cloud-photo-gallery-delete-photo"
  role             = aws_iam_role.photo_lambda.arn
  handler          = "backend.delete_photo.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.photo_lambdas.output_path
  source_code_hash = data.archive_file.photo_lambdas.output_base64sha256
  timeout          = 15

  environment { variables = local.lambda_environment }
}

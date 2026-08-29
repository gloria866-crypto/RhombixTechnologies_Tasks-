# Step 7: least-privilege execution role shared by the photo Lambda functions.
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "photo_lambda" {
  name               = "cloud-photo-gallery-lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "photo_lambda_logs" {
  role       = aws_iam_role.photo_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy_document" "photo_lambda_access" {
  statement {
    sid       = "ListPhotoBucket"
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.photos.arn]
  }

  statement {
    sid    = "ManagePhotoObjects"
    effect = "Allow"
    actions = [
      "s3:DeleteObject",
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = ["${aws_s3_bucket.photos.arn}/users/*"]
  }

  statement {
    sid    = "ManagePhotoMetadata"
    effect = "Allow"
    actions = [
      "dynamodb:DeleteItem",
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:Query",
    ]
    resources = [
      aws_dynamodb_table.photo_metadata.arn,
      "${aws_dynamodb_table.photo_metadata.arn}/index/*",
    ]
  }
}

resource "aws_iam_role_policy" "photo_lambda_access" {
  name   = "cloud-photo-gallery-data-access"
  role   = aws_iam_role.photo_lambda.id
  policy = data.aws_iam_policy_document.photo_lambda_access.json
}

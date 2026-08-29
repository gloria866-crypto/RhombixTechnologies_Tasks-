output "frontend_bucket_name" {
  description = "The S3 bucket reserved for frontend assets in a later step."
  value       = aws_s3_bucket.frontend.bucket
}

output "photos_bucket_name" {
  description = "Set this as PHOTO_BUCKET_NAME for the backend."
  value       = aws_s3_bucket.photos.bucket
}

output "photos_bucket_arn" {
  value = aws_s3_bucket.photos.arn
}

output "photo_metadata_table_name" {
  description = "Use this table name in the Lambda functions added in Step 5."
  value       = aws_dynamodb_table.photo_metadata.name
}

output "photo_metadata_table_arn" {
  value = aws_dynamodb_table.photo_metadata.arn
}

output "api_endpoint" {
  description = "Base URL for the HTTP API."
  value       = aws_apigatewayv2_api.photo_gallery.api_endpoint
}

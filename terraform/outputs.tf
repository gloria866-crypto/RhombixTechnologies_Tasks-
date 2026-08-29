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

variable "aws_region" {
  description = "AWS region for the photo gallery resources."
  type        = string
  default     = "us-east-1"
}

variable "frontend_bucket_name" {
  description = "Globally unique name for the bucket that will host the gallery frontend."
  type        = string
  default     = "photos-gallery-frontend-gloria-2026"
}

variable "photos_bucket_name" {
  description = "Globally unique name for the private bucket that will store uploaded photos."
  type        = string
  default     = "photos-gallery-s3-bucket-gloria-2026"
}

variable "photo_metadata_table_name" {
  description = "DynamoDB table that stores metadata for uploaded photos."
  type        = string
  default     = "PhotoMetadata"
}

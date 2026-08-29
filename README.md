# Cloud Photo Gallery

This project is being built in stages. Step 2 provisions two S3 buckets: one reserved for future frontend assets and one private bucket for uploaded photos.

## Step 2: provision the buckets

From `terraform/`, run:

```powershell
terraform init
terraform apply
```

The defaults are `photos-gallery-frontend-gloria-2026` and `photos-gallery-s3-bucket-gloria-2026`. If either name is unavailable globally, change its value in `terraform/variables.tf` before applying. The photo bucket blocks public access, enables bucket versioning, and enables server-side encryption. The frontend bucket remains private until the CloudFront step.

## Step 4: photo metadata

`terraform/dynamodb.tf` defines the `PhotoMetadata` DynamoDB table. It stores photo details such as `photoId`, `userId`, filename, title, description, category, S3 key, and creation date; only `photoId` is the table's required primary-key attribute. Image files remain in S3.

## Step 5: Lambda handlers

The Python handlers in `backend/` are ready to be attached to API Gateway in the next step:

- `generate_upload_url.lambda_handler` creates a photo metadata record and returns a 15-minute S3 `PUT` URL.
- `get_photos.lambda_handler` returns photo metadata for a `userId` using the `UserPhotosIndex` DynamoDB index.
- `delete_photo.lambda_handler` removes a user's S3 image and its metadata record.

They require `PHOTOS_BUCKET_NAME` and `PHOTO_METADATA_TABLE_NAME` environment variables. The API Gateway routes will be added in Step 6.

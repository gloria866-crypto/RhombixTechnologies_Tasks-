# Cloud Photo Gallery

This project is being built in stages. Step 2 provisions two S3 buckets: one reserved for future frontend assets and one private bucket for uploaded photos.

## Step 2: provision the buckets

From `terraform/`, run:

```powershell
terraform init
terraform apply
```

The defaults are `photos-gallery-frontend-gloria-2026` and `photos-gallery-s3-bucket-gloria-2026`. If either name is unavailable globally, change its value in `terraform/variables.tf` before applying. The photo bucket blocks public access, enables bucket versioning, and enables server-side encryption. The frontend bucket remains private until the CloudFront step.

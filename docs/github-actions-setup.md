# GitHub Actions setup

## CI

The repository runs validation automatically for changes on `dev`, `main`, and pull requests:

- `terraform.yml` checks formatting and validates Terraform.
- `frontend-ci.yml` confirms the frontend files exist and checks JavaScript syntax.

## CD: deploy the frontend

The `deploy-frontend.yml` workflow runs after frontend changes are merged into `main`, or when manually dispatched. It uses temporary GitHub OIDC credentials; do not add long-lived AWS keys to this repository.

Before enabling a deployment, configure these repository settings:

1. Create an AWS IAM OIDC provider for `token.actions.githubusercontent.com` and an IAM role that trusts this repository's `main` branch. We will add this role to Terraform during the IAM step.
2. Give that role only `s3:PutObject`, `s3:DeleteObject`, and `s3:ListBucket` permissions for the frontend bucket.
3. In **Settings → Secrets and variables → Actions**, add:
   - Secret: `AWS_ROLE_TO_ASSUME` — the IAM role ARN.
   - Variable: `AWS_REGION` — for example, `us-east-1`.
   - Variable: `FRONTEND_BUCKET_NAME` — `photos-gallery-frontend-gloria-2026`.
4. In **Settings → Environments**, create `production` and configure a required reviewer if you want approval before deployment.

CloudFront cache invalidation will be added with CloudFront in Step 8.

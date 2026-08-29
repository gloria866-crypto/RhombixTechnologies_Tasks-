# GitHub Actions setup

## Unified CI/CD workflow

`.github/workflows/deploy.yml` is the only workflow file. It runs validation automatically for changes on `dev`, `main`, and pull requests. It deploys only after a successful push to `main`.

- The validation job checks Terraform formatting/configuration and frontend JavaScript syntax.
- The deployment job creates or reuses a private, versioned Terraform state bucket, applies every resource in `terraform/`, and syncs `frontend/` to the frontend bucket output by Terraform.

## CD: deploy the frontend

The deployment job uses GitHub Actions secrets for AWS credentials. Never store credentials in the repository itself.

Before enabling a deployment, configure these repository settings:

1. Create a dedicated IAM user with least-privilege permissions for the Terraform state bucket, the frontend bucket, and every AWS resource Terraform currently manages. Add only the scoped permissions needed as Lambda, API Gateway, CloudFront, IAM, and monitoring resources are added.
2. In **Settings → Secrets and variables → Actions**, add:
   - Secret: `AWS_ACCESS_KEY_ID`
   - Secret: `AWS_SECRET_ACCESS_KEY`
3. The state bucket defaults to `photos-gallery-terraform-state-gloria-2026`. If that globally unique name is unavailable, change `TF_STATE_BUCKET` in `deploy.yml` before merging to `main`.
4. In **Settings → Environments**, create `production` and configure a required reviewer if you want approval before deployment.

CloudFront cache invalidation will be added with CloudFront in Step 8.

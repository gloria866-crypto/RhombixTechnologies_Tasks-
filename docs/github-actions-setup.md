# GitHub Actions setup

## Unified CI/CD workflow

`.github/workflows/deploy.yml` is the only workflow file. It runs validation automatically for changes on `dev`, `main`, and pull requests. It deploys only after a successful push to `main`.

- The validation job checks Terraform formatting/configuration and frontend JavaScript syntax.
- The deployment job creates or reuses a private, versioned Terraform state bucket, applies every resource in `terraform/`, and syncs `frontend/` to the frontend bucket output by Terraform.

## CD: deploy the frontend

The deployment job uses temporary GitHub OIDC credentials; do not add long-lived AWS keys to this repository.

Before enabling a deployment, configure these repository settings:

1. Create an AWS IAM OIDC provider for `token.actions.githubusercontent.com` and an IAM role that trusts this repository's `main` branch. We will add this role to Terraform during the IAM step.
2. Give that role least-privilege permissions for the Terraform state bucket, the frontend bucket, and every AWS resource Terraform currently manages. The role will need additional scoped permissions as Lambda, API Gateway, CloudFront, IAM, and monitoring resources are added.
3. In **Settings → Secrets and variables → Actions**, add:
   - Secret: `AWS_ROLE_TO_ASSUME` — the IAM role ARN.
4. The state bucket defaults to `photos-gallery-terraform-state-gloria-2026`. If that globally unique name is unavailable, change `TF_STATE_BUCKET` in `deploy.yml` before merging to `main`.
5. In **Settings → Environments**, create `production` and configure a required reviewer if you want approval before deployment.

CloudFront cache invalidation will be added with CloudFront in Step 8.

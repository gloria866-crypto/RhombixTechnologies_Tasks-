terraform {
  backend "s3" {
    bucket = "photos-gallery-terraform-state-gloria-2026"
    key    = "cloud-photo-gallery/terraform.tfstate"
    region = "us-east-1"
  }
}

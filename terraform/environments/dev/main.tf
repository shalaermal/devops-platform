terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

module "s3" {
  source = "../../modules/s3"

  bucket_name = "devops-platform-ermal-2026"
  environment = "dev"
}

module "ecr" {
  source = "../../modules/ecr"

  repository_names = ["frontend", "api", "worker"]
  environment      = "dev"
}

module "iam" {
  source = "../../modules/iam"

  environment         = "dev"
  github_org          = "shalaermal"
  github_repo         = "devops-platform"
  ecr_repository_arns = [for url in module.ecr.repository_urls : "arn:aws:ecr:eu-central-1:211125687060:repository/${url}"]
  s3_bucket_arn       = module.s3.bucket_arn
}
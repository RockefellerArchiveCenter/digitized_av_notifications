terraform {
    required_providers {
        aws = {
            version = "~> 4.58"
            source  = "hashicorp/aws"
        }
    }
}

terraform {
  backend "s3" {
    bucket = "rac-terraform-state-backend"
    key    = "digitized-av-notifications/dev"
    region = "us-east-1"
    dynamodb_table = "terraform_state"
    shared_credentials_file = "~/.aws/credentials"
    profile                 = "digitized-av"
  }
}

provider "aws" {
    region =                  "us-east-1"
    shared_credentials_files = ["~/.aws/credentials"]
    profile                  = "digitized-av"
}
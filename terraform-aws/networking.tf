data "terraform_remote_state" "networking" {
  backend = "s3"

  config = {
    bucket  = "shortnd-terraform-state-723732457731"
    key     = "networking/terraform.tfstate"
    region  = "us-east-1"
    profile = "shortndTerraform"
    encrypt = true
  }
}
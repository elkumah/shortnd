terraform {
  backend "s3" {
    bucket       = "shortnd-terraform-state-723732457731"
    key          = "networking/terraform.tfstate"
    region       = "us-east-1"
    profile      = "shortndTerraform"
    encrypt      = true
    use_lockfile = true
  }
}
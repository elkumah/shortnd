resource "aws_ecr_repository" "shortnd_api" {
  name = "shortnd-api"

  image_scanning_configuration {
    scan_on_push = true
  }
  encryption_configuration {
    encryption_type = "AES256"
  }

  image_tag_mutability = "IMMUTABLE"

  tags = {
    Name        = "shortnd-ecr"
    Environment = "dev"
    Project     = "shortnd"
  }
}
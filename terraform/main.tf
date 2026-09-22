resource "aws_vpc" "shortnd" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name        = "shortnd-vpc"
    Environment = "dev"
    Project     = "shortnd"
  }
}

resource "aws_internet_gateway" "shortnd" {
  vpc_id = aws_vpc.shortnd.id
  tags = {
    Name        = "shortnd-igw"
    Environment = "dev"
    Project     = "shortnd"
  }
}
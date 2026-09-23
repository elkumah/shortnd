resource "aws_subnet" "public_1a" {
  vpc_id                  = aws_vpc.shortnd.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name        = "shortnd-public-subnet-a"
    Environment = "dev"
    Project     = "shortnd"
    Tier        = "public"
  }
}

resource "aws_subnet" "public_1b" {
  vpc_id                  = aws_vpc.shortnd.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
  tags = {
    Name        = "shortnd-public-subnet-b"
    Environment = "dev"
    Project     = "shortnd"
    Tier        = "public"
  }
}
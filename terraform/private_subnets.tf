resource "aws_subnet" "private_1a" {
  vpc_id            = aws_vpc.shortnd.id
  cidr_block        = "10.0.11.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name        = "shortnd-private-1a"
    Environment = "dev"
    Project     = "shortnd"
    Tier        = "private"
  }
}

resource "aws_subnet" "private_1b" {
  vpc_id            = aws_vpc.shortnd.id
  cidr_block        = "10.0.12.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name        = "shortnd-private-1b"
    Environment = "dev"
    Project     = "shortnd"
    Tier        = "private"
  }
}

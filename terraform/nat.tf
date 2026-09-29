resource "aws_eip" "nat" {
  domain = "vpc"
  tags = {
    Name        = "shortnd-nat-eip"
    Environment = "dev"
    Project     = "shortnd"
  }
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_1a.id
  tags = {
    Name        = "shortnd-nat-gateway"
    Environment = "dev"
    Project     = "shortnd"
  }

  depends_on = [aws_internet_gateway.shortnd]
}
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
    Name        = "shortnd-nat"
    Environment = "dev"
    Project     = "shortnd"
  }

  depends_on = [
    aws_internet_gateway.shortnd
  ]
}

resource "aws_route" "private_nat" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat.id
}
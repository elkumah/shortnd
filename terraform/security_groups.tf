resource "aws_security_group" "load_balancer" {
  name        = "shortnd-lb-sg"
  description = "Security group for shortnd public load balancer"
  vpc_id      = aws_vpc.shortnd.id

  tags = {
    Name        = "shortnd-lb-sg"
    Environment = "dev"
    Project     = "shortnd"
    Tier        = "public"
  }
}

resource "aws_security_group" "api" {
  name        = "shortnd-api-sg"
  description = "Security group for shortnd api"
  vpc_id      = aws_vpc.shortnd.id

  tags = {
    Name        = "shortnd-api-sg"
    Environment = "dev"
    Project     = "shortnd"
    Tier        = "private"
  }
}

resource "aws_security_group" "db" {
  name        = "shortnd-db-sg"
  description = "Security group for shortnd db"
  vpc_id      = aws_vpc.shortnd.id

  tags = {
    Name        = "shortnd-db-sg"
    Environment = "dev"
    Project     = "shortnd"
    Tier        = "private"
  }
}
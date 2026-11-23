resource "aws_security_group" "alb" {
  name        = "shortnd-lb-sg"
  description = "Security group for shortnd application load balancer"
  vpc_id      = aws_vpc.shortnd.id

  tags = {
    Name        = "shortnd-lb-sg"
    Environment = "dev"
    Project     = "shortnd"
    Tier        = "public"
  }
}

# EKS Worker Nodes Security Group
resource "aws_security_group" "eks_nodes" {
  name        = "shortnd-eks-node-sg"
  description = "Security group for Shortnd EKS worker nodes"
  vpc_id      = aws_vpc.shortnd.id

  tags = {
    Name        = "shortnd-eks-node-sg"
    Environment = "dev"
    Project     = "shortnd"
  }
}

# RDS PostgreSQL Security Group
resource "aws_security_group" "rds" {
  name        = "shortnd-rds-sg"
  description = "Security group for Shortnd PostgreSQL database"
  vpc_id      = aws_vpc.shortnd.id

  tags = {
    Name        = "shortnd-rds-sg"
    Environment = "dev"
    Project     = "shortnd"
  }
}
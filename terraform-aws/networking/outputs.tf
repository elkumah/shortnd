# VPC
output "vpc_id" {
  description = "ID of the Shortnd VPC"
  value       = aws_vpc.shortnd.id
}

# Public subnets
output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value = [
    aws_subnet.public_1a.id,
    aws_subnet.public_1b.id
  ]
}

# Private subnets
output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value = [
    aws_subnet.private_1a.id,
    aws_subnet.private_1b.id
  ]
}

# Security groups
output "alb_security_group_id" {
  description = "ID of the ALB security group"
  value       = aws_security_group.alb.id
}

output "eks_node_security_group_id" {
  description = "ID of the EKS node security group"
  value       = aws_security_group.eks_nodes.id
}

output "rds_security_group_id" {
  description = "ID of the RDS security group"
  value       = aws_security_group.rds.id
}
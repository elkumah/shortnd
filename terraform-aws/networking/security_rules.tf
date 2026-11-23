# Allow HTTP traffic from the internet
resource "aws_vpc_security_group_ingress_rule" "alb_http" {
  security_group_id = aws_security_group.alb.id

  description = "Allow HTTP traffic from the internet"
  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 80
  to_port     = 80
  ip_protocol = "tcp"
}

# Allow HTTPS traffic from the internet
resource "aws_vpc_security_group_ingress_rule" "alb_https" {
  security_group_id = aws_security_group.alb.id

  description = "Allow HTTPS traffic from the internet"
  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}

# Allow communication between EKS worker nodes
resource "aws_vpc_security_group_ingress_rule" "eks_nodes_internal" {
  security_group_id = aws_security_group.eks_nodes.id

  description                  = "Allow communication between EKS worker nodes"
  referenced_security_group_id = aws_security_group.eks_nodes.id
  ip_protocol                  = "-1"
}
# Allow PostgreSQL traffic from EKS worker nodes
resource "aws_vpc_security_group_ingress_rule" "rds_postgresql" {
  security_group_id = aws_security_group.rds.id

  description                  = "Allow PostgreSQL traffic from EKS worker nodes"
  referenced_security_group_id = aws_security_group.eks_nodes.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}
# Allow EKS worker nodes to access external services
resource "aws_vpc_security_group_egress_rule" "eks_nodes_outbound" {
  security_group_id = aws_security_group.eks_nodes.id

  description = "Allow outbound traffic from EKS worker nodes"
  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "-1"
}
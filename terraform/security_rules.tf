resource "aws_vpc_security_group_ingress_rule" "load_balancer_http" {
  security_group_id = aws_security_group.load_balancer.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  to_port           = 80
  ip_protocol       = "tcp"

  description = "Allow HTTP traffic from anywhere to the load balancer"
}

resource "aws_vpc_security_group_ingress_rule" "load_balancer_https" {
  security_group_id = aws_security_group.load_balancer.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 443
  to_port           = 443
  ip_protocol       = "tcp"
  description       = "Allow HTTPS traffic from anywhere to the load balancer"
}

resource "aws_vpc_security_group_ingress_rule" "api_from_lb" {
  security_group_id            = aws_security_group.api.id
  referenced_security_group_id = aws_security_group.load_balancer.id

  from_port   = 8000
  to_port     = 8000
  ip_protocol = "tcp"
  description = "Allow API traffic from the load balancer"
}

resource "aws_vpc_security_group_ingress_rule" "db_from_api" {
  security_group_id            = aws_security_group.db.id
  referenced_security_group_id = aws_security_group.api.id

  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"

  description = "Allow PostgreSQL traffic from the Shortnd API"
}
resource "aws_vpc_security_group_egress_rule" "load_balancer_to_api" {
  security_group_id            = aws_security_group.load_balancer.id
  referenced_security_group_id = aws_security_group.api.id

  from_port   = 8000
  to_port     = 8000
  ip_protocol = "tcp"

  description = "Allow load balancer traffic to the Shortnd API"
}
resource "aws_vpc_security_group_egress_rule" "api_to_db" {
  security_group_id            = aws_security_group.api.id
  referenced_security_group_id = aws_security_group.db.id

  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"

  description = "Allow API traffic to PostgreSQL"
}

resource "aws_vpc_security_group_egress_rule" "api_https" {
  security_group_id = aws_security_group.api.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"

  description = "Allow API outbound HTTPS traffic"
}
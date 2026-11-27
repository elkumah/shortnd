# DB subnet group for Shortnd PostgreSQL
resource "aws_db_subnet_group" "shortnd" {
  name        = "shortnd-db-subnet-group"
  description = "Private subnet group for Shortnd PostgreSQL database"

  subnet_ids = data.terraform_remote_state.networking.outputs.private_subnet_ids

  tags = {
    Name        = "shortnd-db-subnet-group"
    Environment = "dev"
    Project     = "shortnd"
  }
}
# PostgreSQL database instance
resource "aws_db_instance" "shortnd" {
  identifier = "shortnd-postgres"

  engine         = "postgres"
  instance_class = "db.t3.micro"

  allocated_storage     = 20
  max_allocated_storage = 50
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name                     = "shortnd"
  username                    = var.db_username
  manage_master_user_password = true
  port                        = 5432

  db_subnet_group_name = aws_db_subnet_group.shortnd.name
  vpc_security_group_ids = [
    data.terraform_remote_state.networking.outputs.rds_security_group_id
  ]

  publicly_accessible = false
  multi_az            = false

  backup_retention_period = 7
  copy_tags_to_snapshot   = true

  auto_minor_version_upgrade = true
  deletion_protection        = true
  skip_final_snapshot        = false

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    Name        = "shortnd-postgres"
    Environment = "dev"
    Project     = "shortnd"
  }
}
# Allow PostgreSQL connections from the EKS cluster security group
resource "aws_vpc_security_group_ingress_rule" "rds_from_eks_cluster" {
  security_group_id = data.terraform_remote_state.networking.outputs.rds_security_group_id

  description                  = "Allow PostgreSQL traffic from EKS cluster nodes"
  referenced_security_group_id = aws_eks_cluster.shortnd.vpc_config[0].cluster_security_group_id

  from_port   = 5432
  to_port     = 5432
  ip_protocol = "tcp"
}
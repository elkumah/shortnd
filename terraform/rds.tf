# DB subnet group for Shortnd PostgreSQL
resource "aws_db_subnet_group" "shortnd" {
  name        = "shortnd-db-subnet-group"
  description = "Private subnet group for Shortnd PostgreSQL"

  subnet_ids = [
    aws_subnet.private_1a.id,
    aws_subnet.private_1b.id
  ]

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

  db_subnet_group_name   = aws_db_subnet_group.shortnd.name
  vpc_security_group_ids = [aws_security_group.db.id]

  publicly_accessible = false
  multi_az            = false

  backup_retention_period = 7
  copy_tags_to_snapshot   = true

  auto_minor_version_upgrade = true
  deletion_protection        = false
  skip_final_snapshot        = true

  tags = {
    Name        = "shortnd-postgres"
    Environment = "dev"
    Project     = "shortnd"
  }
}
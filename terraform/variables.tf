variable "aws_region" {
  description = "AWS region where Shortnd infra will be deployed"
  type        = string
  default     = "us-east-1"
}
variable "eks_cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "shortnd-eks"
}

variable "eks_kubernetes_version" {
  description = "Kubernetes version for the EKS cluster"
  type        = string
}

variable "eks_public_address_cidr" {
  description = "CIDR block for the public address of the EKS cluster"
  type        = list(string)
}
variable "db_username" {
  description = "Master username for the Shortnd PostgreSQL database"
  type        = string
  sensitive   = true
}


resource "aws_eks_cluster" "shortnd" {
  name                          = var.eks_cluster_name
  role_arn                      = aws_iam_role.eks_cluster.arn
  version                       = var.eks_kubernetes_version
  deletion_protection           = true
  bootstrap_self_managed_addons = false

  access_config {
    authentication_mode                         = "API"
    bootstrap_cluster_creator_admin_permissions = true
  }

  vpc_config {
    subnet_ids = data.terraform_remote_state.networking.outputs.private_subnet_ids

    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = var.eks_public_address_cidr

  }

  enabled_cluster_log_types = [
    "api",
    "audit",
    "authenticator",
    "controllerManager",
    "scheduler"
  ]
  tags = {
    Name        = "shortnd-eks"
    Environment = "dev"
    Project     = "shortnd"
  }

  depends_on = [aws_iam_role_policy_attachment.eks_cluster_policy]
}
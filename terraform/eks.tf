resource "aws_eks_cluster" "shortnd" {
  name     = var.eks_cluster_name
  role_arn = aws_iam_role.eks_cluster.arn
  version  = var.eks_kubernetes_version

  vpc_config {
    subnet_ids = [

      aws_subnet.private_1a.id,
      aws_subnet.private_1b.id
    ]

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
resource "aws_eks_addon" "vpc_cni" {
  cluster_name  = aws_eks_cluster.shortnd.name
  addon_name    = "vpc-cni"
  addon_version = "v1.22.4-eksbuild.14"

  service_account_role_arn = aws_iam_role.vpc_cni.arn

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "PRESERVE"

  depends_on = [
    aws_iam_role_policy_attachment.vpc_cni
  ]

  tags = {
    Name        = "shortnd-vpc-cni"
    Environment = "dev"
    Project     = "shortnd"
  }
}

resource "aws_eks_addon" "coredns" {
  cluster_name  = aws_eks_cluster.shortnd.name
  addon_name    = "coredns"
  addon_version = "v1.14.7-eksbuild.35"

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "PRESERVE"

  depends_on = [
    aws_eks_node_group.shortnd
  ]

  tags = {
    Name        = "shortnd-coredns"
    Environment = "dev"
    Project     = "shortnd"
  }
}

resource "aws_eks_addon" "kube_proxy" {
  cluster_name  = aws_eks_cluster.shortnd.name
  addon_name    = "kube-proxy"
  addon_version = "v1.37.0-eksbuild.39"

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "PRESERVE"

  depends_on = [
    aws_eks_node_group.shortnd
  ]

  tags = {
    Name        = "shortnd-kube-proxy"
    Environment = "dev"
    Project     = "shortnd"
  }
}
resource "aws_eks_node_group" "shortnd" {
  cluster_name    = aws_eks_cluster.shortnd.name
  node_group_name = "shortnd-eks-node"
  node_role_arn   = aws_iam_role.eks_node.arn
  subnet_ids      = data.terraform_remote_state.networking.outputs.private_subnet_ids

  scaling_config {
    desired_size = 1
    max_size     = 1
    min_size     = 1
  }
  update_config {
    max_unavailable = 1
  }

  instance_types = ["t3.small"]

  tags = {
    Name        = "shortnd-eks-node-group"
    Environment = "dev"
    Project     = "shortnd"
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_node_worker,
    aws_iam_role_policy_attachment.eks_node_cni,
    aws_iam_role_policy_attachment.eks_node_ecr,
    aws_eks_addon.vpc_cni
  ]
}
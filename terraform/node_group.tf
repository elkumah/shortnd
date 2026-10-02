resource "aws_eks_node_group" "shortnd" {
  cluster_name    = aws_eks_cluster.shortnd.name
  node_group_name = "shortnd-eks-node"
  node_role_arn   = aws_iam_role.eks_node.arn
  subnet_ids      = [aws_subnet.private_1a.id, aws_subnet.private_1b.id]

  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
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
  ]
}
locals {
  eks_oidc_issuer = trimprefix(
    aws_eks_cluster.shortnd.identity[0].oidc[0].issuer,
    "https://"
  )
}

resource "aws_iam_role" "vpc_cni" {
  name = "shortnd-vpc-cni-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Federated = aws_iam_openid_connect_provider.eks.arn
        }

        Action = "sts:AssumeRoleWithWebIdentity"

        Condition = {
          StringEquals = {
            "${local.eks_oidc_issuer}:aud" = "sts.amazonaws.com"

            "${local.eks_oidc_issuer}:sub" = "system:serviceaccount:kube-system:aws-node"
          }
        }
      }
    ]
  })

  tags = {
    Name        = "shortnd-vpc-cni-role"
    Environment = "dev"
    Project     = "shortnd"
  }
}

resource "aws_iam_role_policy_attachment" "vpc_cni" {
  role       = aws_iam_role.vpc_cni.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}
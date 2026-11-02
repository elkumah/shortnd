# IAM policy allowing the Shortnd API to retrieve its RDS credentials
resource "aws_iam_policy" "shortnd_api_secrets" {
  name        = "shortnd-api-secrets-policy"
  description = "Allow the Shortnd API to retrieve its RDS credentials"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "secretsmanager:GetSecretValue"
        ]

        Resource = aws_db_instance.shortnd.master_user_secret[0].secret_arn
      }
    ]
  })

  tags = {
    Name        = "shortnd-api-secrets-policy"
    Environment = "dev"
    Project     = "shortnd"
  }
}
# IAM role trusted by the Shortnd API Kubernetes service account
resource "aws_iam_role" "shortnd_api" {
  name = "shortnd-api-secrets-role"

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
            "${replace(aws_eks_cluster.shortnd.identity[0].oidc[0].issuer, "https://", "")}:aud" = "sts.amazonaws.com"

            "${replace(aws_eks_cluster.shortnd.identity[0].oidc[0].issuer, "https://", "")}:sub" = "system:serviceaccount:shortnd:shortnd-api"
          }
        }
      }
    ]
  })

  tags = {
    Name        = "shortnd-api-secrets-role"
    Environment = "dev"
    Project     = "shortnd"
  }
}
# Attach the least-privilege policy to the API role
resource "aws_iam_role_policy_attachment" "shortnd_api_secrets" {
  role       = aws_iam_role.shortnd_api.name
  policy_arn = aws_iam_policy.shortnd_api_secrets.arn
}
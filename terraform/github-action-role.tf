data "aws_caller_identity" "current" {}

resource "aws_iam_role" "github_actions" {
  name = "shortnd-github-actions-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        }

        Action = "sts:AssumeRoleWithWebIdentity"

        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }

          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:elkumah/shortnd:*"
          }
        }
      }
    ]
  })

  tags = {
    Name        = "shortnd-github-actions-role"
    Environment = "dev"
    Project     = "shortnd"
  }
}
output "github_actions_role_arn" {
  description = "ARN i GitHub Actions role"
  value       = aws_iam_role.github_actions.arn
}
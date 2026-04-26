variable "repository_names" {
  description = "Lista e emrave te ECR repositories"
  type        = list(string)
}

variable "environment" {
  description = "Environment (dev, prod)"
  type        = string
}
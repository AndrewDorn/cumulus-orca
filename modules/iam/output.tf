output "restore_object_role_arn" {
  value = aws_iam_role.restore_object_role.arn
}

output "request_status_role_arn" {
  value = aws_iam_role.request_status_object_role.arn
}
output "usernames" {
  value = { for user, profile in aws_iam_user_login_profile.profile : user => profile.user }
}

output "passwords" {
  value = { for user, profile in aws_iam_user_login_profile.profile : user => profile.password }
}

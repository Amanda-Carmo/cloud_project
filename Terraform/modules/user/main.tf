# Create IAM user for each user in list
resource "aws_iam_user" "user" {
    for_each = { for user in var.users : user.name => user }
    name = each.value.name
}

# Create login profile for each user
resource "aws_iam_user_login_profile" "profile" {
    for_each = { for user in var.users : user.name => user }
    user = aws_iam_user.user[each.value.name].name
    password_length = 13
    password_reset_required = true
}

# Create access key for each user
resource "aws_iam_access_key" "access_key" {
    for_each = { for user in var.users : user.name => user }
    user = aws_iam_user.user[each.value.name].name
}

# Create the inline policy for each user
data "aws_iam_policy_document" "policy_doc" {
    for_each = { for user in var.users : user.name => user }
    policy_id = each.value.name
    statement {
      effect = "Allow"
        sid = "VisualEditor0"
        actions = each.value.restrictions.actions
        resources = each.value.restrictions.resources
    }
}

# Create the policy for each user
resource "aws_iam_policy" "policy" {
    for_each = { for user in var.users : user.name => user }
    name = each.value.restrictions.name
    description = each.value.restrictions.description
    policy = data.aws_iam_policy_document.policy_doc[each.value.name].json
}

# Attach the policy to the users
resource "aws_iam_user_policy_attachment" "policy_attach" {
    for_each = { for user in var.users : user.name => user }
    user = aws_iam_user.user[each.value.name].name
    policy_arn = aws_iam_policy.policy[each.value.name].arn
}
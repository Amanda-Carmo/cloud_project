output "instance_eip" {
    value = {for instance, ec2 in aws_eip.eip: instance => ec2.public_ip}
}

output "instance" {
    value = aws_instance.instance
}

output "security_groups" {
    value = [for sg in aws_security_group.sg: sg]
}
output "vpc_id" {
    value = aws_vpc.vpc.id
}
  
output "vpc_cidr" {
    value = aws_vpc.vpc.cidr_block
}

output "public_subnet" {
    value = aws_subnet.public_subnet.id
}

output "security_groups" {
    value = [for sg in aws_security_group.sg: sg]
}
  
output "availability_zones" {
    value = data.aws_availability_zones.available.names
}
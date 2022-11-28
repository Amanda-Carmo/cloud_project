# Get Availability Zones
resource "tls_private_key" "pk" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Create Security Groups 
# resource "aws_security_group" "sg" {
#     for_each = { for sg in var.security_groups : sg.name => sg }
#     name = each.value.name
#     description = each.value.description
#     vpc_id = var.vpc_id
    
#     dynamic "ingress" {
#         for_each = each.value.ingress
#         content {
#             from_port = ingress.value.from_port
#             to_port = ingress.value.to_port
#             protocol = ingress.value.protocol
#             cidr_blocks = ingress.value.cidr_blocks
#         }
#     }

#     dynamic "egress" {
#         for_each = each.value.egress
#         content {
#             from_port = egress.value.from_port
#             to_port = egress.value.to_port
#             protocol = egress.value.protocol
#             cidr_blocks = egress.value.cidr_blocks
#         }
#     }

#     tags = {
#         Name = each.value.name
#         id = each.value.id
#     }
# }

# Create instances 
resource "aws_instance" "instance" {
    for_each = {for instance in var.instances: instance.name => instance}
    ami = each.value.ami
    
    instance_type = each.value.size
    key_name = each.value.name
    subnet_id = var.public_subnet
    vpc_security_group_ids = [
        for sg in var.security_groups:
            sg.id if contains(each.value.security_groups_ids, sg.id)
        ]
    
    tags = {
        Name = each.value.name
    }
}

# Create pem file for each instance
resource "aws_key_pair" "kp" {
    for_each = {for instance in var.instances: instance.name => instance}
    key_name = each.value.name
    public_key = tls_private_key.pk.public_key_openssh

    provisioner "local-exec" {
        command = "echo '${tls_private_key.pk.private_key_pem}' > '${path.module}/keys/${each.value.name}.pem'"
    }
}

# Create Elastic IP for each instance
resource "aws_eip" "eip" {
    for_each = {for instance in var.instances: instance.name => instance}
    vpc = true
    instance = aws_instance.instance[each.value.name].id
}

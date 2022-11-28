# Configuring the network

# Create a VPC for the region associated
resource "aws_vpc" "vpc" {
    cidr_block = var.vpc_cidr
    enable_dns_hostnames = true
    enable_dns_support = true
    tags = {
        Name = "cloudcasts-${var.infra_env}-vpc"
        Environment = var.infra_env
    } 
    lifecycle {
        create_before_destroy = true
    }
}

# Create a public subnet for each AZ
resource "aws_subnet" "public_subnet" {
    vpc_id = aws_vpc.vpc.id
    cidr_block = cidrsubnet(var.vpc_cidr, 4, 2)

    tags = {
        Name = "${var.infra_env}-public-subnet"
        Role = "public"
        Environment = var.infra_env
    }
}

# Get Availability Zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Create a public route table
resource "aws_route_table" "public_route_table" {
    vpc_id = aws_vpc.vpc.id

    tags = {
      Name = "Public Route Table"
    }
}

# Associate the public route table with the public subnet
resource "aws_route_table_association" "public_route_table_association" {
    subnet_id = aws_subnet.public_subnet.id
    route_table_id = aws_route_table.public_route_table.id
}


# Create a Gateway for the VPC
resource "aws_internet_gateway" "igw" {
    vpc_id = aws_vpc.vpc.id
    tags = {
        Name = "${var.infra_env}-igw"
        Environment = var.infra_env
    }
}

# Create Security Groups each
resource "aws_security_group" "sg" {
    for_each = { for sg in var.security_groups : sg.name => sg }
    name = each.value.name
    description = each.value.description
    vpc_id = aws_vpc.vpc.id

    tags = {
        Name = each.value.name
        id = each.value.id
    }

    dynamic "ingress" {
        for_each = each.value.ingress
        content {
            from_port = ingress.value.from_port
            to_port = ingress.value.to_port
            protocol = ingress.value.protocol
            cidr_blocks = ingress.value.cidr_blocks
        }
    }

    dynamic "egress" {
        for_each = each.value.egress
        content {
            from_port = egress.value.from_port
            to_port = egress.value.to_port
            protocol = egress.value.protocol
            cidr_blocks = egress.value.cidr_blocks
        }
    }
}

variable "instance_root_device_size" {
    type = number
    description = "EC2 server root device size"
    default = 12
}
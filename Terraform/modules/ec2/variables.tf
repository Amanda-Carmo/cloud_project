variable "infra_env" {
    type = string
    description = "Infraestructure environment"
}

# variable "instance_size" {
#     type = string
#     description = "EC2 server size"
#     default = "m1.tiny"
# }

# variable "instance_ami" {
#     type = string
#     description = "EC2 server Image"
# }

# variable "vpc_id" {
#     type = string
#     description = "VPC ID"
# }

# variable "instance_root_device_size" {}

variable "instances"{}
variable "public_subnet"{}
variable "security_groups"{}

variable "vpc_id"{}
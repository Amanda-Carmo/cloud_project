variable "infra_env"{
    type = string
    description = "Infra environment"
}

variable "vpc_cidr"{
    type = string
    description = "The IP range to use for the VPC"  
    default = "10.0.0.0/16"
}

# variable "public_subnet_numbers" {
#     type = map(number)
#     description = "Map AZ to a number that will be used for public subnet"

#     default = {
#         us-east-1  = 1
#         us-east-2a = 2
#         us-west-2c = 3
#     }
  
# }

variable "security_groups"{
    default = []
}

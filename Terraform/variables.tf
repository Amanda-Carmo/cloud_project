variable "infra_env" {
  type        = string
  description = "Infraestructure environment"
}

variable "instances"{
  type = list(object({
      security_groups_ids = list(string)
      name = string
      size = string
      ami = string
      region = string
    }))
}

variable "security_groups" {
  type = list(object({
    id          = string
    name        = string
    description = string
    ingress = list(object({
      from_port   = number
      to_port     = number
      protocol    = string
      cidr_blocks = list(string)
    }))
    egress = list(object({
      from_port   = number
      to_port     = number
      protocol    = string
      cidr_blocks = list(string)
    }))
  }))
  default = [ {
    description = "default security group"
    ingress = [ {
      cidr_blocks = [ "0.0.0.0/0" ]
      from_port = 80
      protocol = "tcp"
      to_port = 80
    } ]
    
    egress = [ {
      cidr_blocks = [ "0.0.0.0/0" ]
      from_port = 22
      protocol = "tcp"
      to_port = 22
    } ]
    id = "1"
    name = "default_sg"
  } ]
}

variable "instance_root_device_size" {
    type = number
    description = "EC2 server root device size"
    default = 12
}

variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

variable "aws_secret_key" {
  type        = string
  description = "AWS secret key"
}

variable "aws_access_key" {
  type = string
  description = "AWS access key"
}

variable "users"{
  description = "List of users"
  type = list(object({
    name = string
    restrictions = object({
      name = string
      description = string
      resources = list(string)
      actions = list(string)
    })
  }))
}
module "vpc" {
    source = "./modules/vpc"

    infra_env = var.infra_env
    vpc_cidr = "10.0.0.0/17"
    # security_groups = var.security_groups
}

module "ec2" {
    source = "./modules/ec2"

    infra_env = var.infra_env
    instances = var.instances
    security_groups = var.security_groups
    public_subnet = module.vpc.public_subnet
    vpc_id = module.vpc.vpc_id
}

module "user" {
    source = "./modules/user"
    users = var.users
}


output "vpc" {
  value = module.vpc
}

output "ec2" {
  value = module.ec2
}

output "user" {
  value = module.user
}
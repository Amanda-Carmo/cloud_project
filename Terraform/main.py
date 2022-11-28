from rich import print as rprint
from rich.console import Console
from rich.prompt import Prompt
from rich.padding import Padding
from rich.prompt import Confirm
import json 
import os
import shortuuid

console = Console()

global user_list

f_user = open('default_variables.json')
read_file = json.load(f_user)
user_list = read_file["users"]
f_user.close()

global instance_list
f_instance = open('default_variables.json')
read_file = json.load(f_instance)
instance_list = read_file["instances"]
f_instance.close()

global sg_list
f_sg = open('default_variables.json')
read_file = json.load(f_sg)

if read_file["security_groups"] is None:
    sg_list = []

else:    
    sg_list = read_file["security_groups"]



f_sg.close()


def create_user():
    rprint("[bold purple]Creating User[/bold purple]")
    username = Prompt.ask("[blue]Username:[/blue]")

    f_user = open('default_variables.json')  
    read_file = json.load(f_user)
    user_list = read_file["users"]

    for i in user_list:
        if i["name"] == username:
            rprint("User already exists")
            return
    f_user.close()

    rprint("[bold purple]Set restrictions for user[/bold purple]")

    # Restriction options
    restriction_actions = []
    rprint("\n")

    restriction_action = Prompt.ask("[blue]Restriction Action:[/blue]")
    restriction_actions.append(restriction_action)

    add_action = Prompt.ask("Add one more action?", choices=["y", "n"])

    while add_action == "y":
        restriction_action = Prompt.ask("[blue]Restriction Action:[/blue]")
        restriction_actions.append(restriction_action)
        add_action = Prompt.ask("Add one more action?", choices=["y", "n"])

    rprint("\n")

    restriction_resources = []
    restriction_resource = Prompt.ask("[blue]Restriction Resource:[/blue]")
    restriction_resources.append(restriction_resource)

    add_resource = Prompt.ask("Add one more resource?", choices=["y", "n"])
    while add_resource == "y":
        restriction_resource = Prompt.ask("[blue]Restriction Resource:[/blue]")
        restriction_resources.append(restriction_resource)
        add_resource = Prompt.ask("Add one more resource?", choices=["y", "n"])

    
    created_users = {
            "name": username, 
            "restrictions": {
                "name": "restriciton" + username,
                "description": f"Restriction for {username}",
                "actions": restriction_actions,
                "resources": restriction_resources,
        }}

    user_list.append(created_users)

    default_data = {
        "users": user_list,
        "instances":instance_list,
        "security_groups": sg_list,
    }

    file = 'default_variables.json'
    with open(file, "w") as f:
        json.dump(default_data, f)
    
    os.system(f"terraform plan -var-file={file}")
    os.system(f"terraform apply -var-file={file}")
    rprint("\n")
    

def create_sg():
    sg_id = str(shortuuid.uuid())[:13]

    print("------------------------------------------")
    rprint("\n")
    rprint("[bold purple]Creating Security Group[/bold purple]")
    sg_name = Prompt.ask("[blue]Security Group Name:[/blue]")
    sg_description = Prompt.ask("[blue]Security Group Description:[/blue]")

    rprint("\n")
    rprint("[bold purple]Security Group rules[/bold purple]")
    rprint("[bold purple]EGRESS[/bold purple]")
    eg_fromport = Prompt.ask("[blue]From Port:[/blue]")
    eg_toport = Prompt.ask("[blue]To Port:[/blue]")
    eg_protocol = Prompt.ask("[blue]Protocol:[/blue]")
    eg_cidr = Prompt.ask("[blue]CIDR:[/blue]")

    rprint("[bold purple]INGRESS[/bold purple]")
    ing_fromport = Prompt.ask("[blue]From Port:[/blue]")
    ing_toport = Prompt.ask("[blue]To Port:[/blue]")
    ing_protocol = Prompt.ask("[blue]Protocol:[/blue]")
    ing_cidr = Prompt.ask("[blue]CIDR:[/blue]")


    created_sg = {
            "id": sg_id,
            "name": sg_name,
            "description": sg_description,
            "ingress": [{
                "from_port": ing_fromport,
                "to_port": ing_toport,
                "protocol": ing_protocol,
                "cidr_blocks": [ing_cidr],
            }],
            "egress": [{
                "from_port": eg_fromport,
                "to_port": eg_toport,
                "protocol": eg_protocol,
                "cidr_blocks": [eg_cidr],
            }]
        }
    
    sg_list.append(created_sg)

    default_data = {
        "users": user_list,
        "instances":instance_list,
        "security_groups": sg_list,
    }


    file = 'default_variables.json'
    with open(file, "w") as f:
        json.dump(default_data, f)
    
    os.system(f"terraform plan -var-file={file}")
    os.system(f"terraform apply -var-file={file}")

    return sg_id

# dict_keys(['Description', 'GroupName', 'IpPermissions', 'OwnerId', 'GroupId', 'IpPermissionsEgress', 'Tags', 'VpcId'])

def create_instance():
    regions = {}

    if not os.path.exists("./terraform.tfstate.d"):
        os.mkdir("./terraform.tfstate.d")

    
    print("--------------------------------------------------")


    rprint("[bold purple]Creating Instance[/bold purple]")
    instance_name = Prompt.ask("[blue]Instance Name:[/blue]")
    instance_type = Prompt.ask("[blue]Instance Type:[/blue]")
    instance_ami = Prompt.ask("[blue]Instance AMI:[/blue]")
    rprint(f"{list(regions.keys())}")
    instance_region = 'us-east-1'


    f = open('default_variables.json')
    read_file = json.load(f)
    instance_sgs = read_file["security_groups"]
    f.close()
    
    print("------------------------------------------")
    rprint("Security Groups created:")
    rprint(f"{instance_sgs}")
    print("------------------------------------------")

    if len(instance_sgs) == 0:
        rprint("There are no security groups created. Please create one first.")
        create_sg()
        f = open('default_variables.json')
        read_file = json.load(f)
        sg_id = read_file["security_groups"][0]["id"]
        print(f"The security group created id is: {sg_id}")
        f.close()

    else:
        rprint("You can get Security Group ID from existing Security Groups or create a new one")

        ask_sg = Prompt.ask("Create Security Group?", choices=["y", "n"])
        if ask_sg == "y":
            create_sg()
            rprint("Security Group created. You canfind the id below")
            f = open('default_variables.json')
            read_file = json.load(f)
            instance_sgs = read_file["security_groups"]
            rprint(instance_sgs)
            f.close()
            print(f"The security group created id is: {sg_id}")
            print("------------------------------------------")

    
    instance_sg_id = Prompt.ask("[blue]Instance Security Group ID:[/blue]")
    print(instance_sg_id)

    # os.system("aws ec2 describe-security-groups --region us-east-1")
    var = os.popen('aws ec2 describe-security-groups --region us-east-1').read()

    varj = json.loads(var)

    var_sg = varj['SecurityGroups']

    print(var_sg)

    for i in var_sg:
        print()
        if 'Tags' in i.keys():

            for j in i['Tags']:
                if j['Value'] == instance_sg_id:
                    sg_id = i['GroupId']
                    print(sg_id)
                    break
            print("------------------------------------------")

    created_inst = {
            "name": instance_name,
            "size": instance_type,
            "ami": instance_ami,
            "security_groups_ids": [instance_sg_id],
            "region": instance_region,
        }

    instance_list.append(created_inst)

    default_data = {
        "users": user_list,
        "instances":instance_list,
        "security_groups":sg_list,
    }

    file = 'default_variables.json'
    with open(file, "w") as f:
        json.dump(default_data, f)
    
    os.system(f"terraform plan -var-file={file}")
    os.system(f"terraform apply -var-file={file}")


def delete_instance(instance_name):
    instance_exists = False
    file = 'default_variables.json'

    del_instance = instance_name
    confirm_delete = Prompt.ask(f"Are you sure you want to delete {instance_name}?", choices=["y", "n"])

    with open(file, 'r', encoding='utf-8') as f: 
        my_list = json.load(f)
        print(my_list)
        
        if confirm_delete == "y" and len(my_list["instances"]) > 0:
            instance_exists = True
            print('Deleting instance...')         
            for idx, obj in enumerate(my_list["instances"]):
                if obj["name"] == del_instance:
                    my_list['instances'].pop(idx)
                    
                    break        

    if instance_exists == True:           
        with open (file, 'w') as f:
            f.write(json.dumps(my_list))

        # os.system(f"terraform plan -var-file={file}")
        os.system(f"terraform apply -var-file={file}")

    else:
        rprint("There are no instances with name: " + instance_name)
    
def delete_user(user_name):
    user_exists = False
    file = 'default_variables.json'

    del_user = user_name
    confirm_delete = Prompt.ask(f"Are you sure you want to delete {user_name}?", choices=["y", "n"])

    with open(file, 'r', encoding='utf-8') as f: 
        my_list = json.load(f)
        print(my_list)
        
        if confirm_delete == "y" and len(my_list["users"]) > 0:
            user_exists = True
            print('Deleting user...')         
            for idx, obj in enumerate(my_list["users"]):
                if obj["name"] == del_user:
                    my_list['users'].pop(idx)
                    
                    break        

    if user_exists == True:           
        with open (file, 'w') as f:
            f.write(json.dumps(my_list))

        # os.system(f"terraform plan -var-file={file}")
        os.system(f"terraform apply -var-file={file}")

    else:
        rprint("There are no users with name: " + user_name)



def delete_sg(sg_name):
    sg_exists = False
    file = 'default_variables.json'

    del_sg = sg_name
    confirm_delete = Prompt.ask(f"Are you sure you want to delete {sg_name}?", choices=["y", "n"])

    with open(file, 'r', encoding='utf-8') as f: 
        my_list = json.load(f)
        print(my_list)
        
        if confirm_delete == "y" and len(my_list["security_groups"]) > 0:
            sg_exists = True
            print('Deleting Security Group...')         
            for idx, obj in enumerate(my_list["security_groups"]):
                if obj["name"] == del_sg:

                    my_list['security_groups'].pop(idx)
                    
                    break       

    
    if sg_exists == True:
        with open (file, 'w') as f:
            f.write(json.dumps(my_list))

        # os.system(f"terraform plan -var-file={file}")
        os.system(f"terraform apply -var-file={file}")

    else:
        rprint("There are no security groups with name: " + sg_name)
        

if not os.path.exists("./.terraform"):
    os.system(f"terraform init")


options = Prompt.ask("Choose action:", choices=["create", "delete", 'list'])
if options == "create":
    options_create = Prompt.ask("Create:", choices=["user", "security group", 'instance', 'exit'])
    if options_create == "security group":
        create_sg()

    if options_create == "user":
        create_user()

    if options_create == "instance":
        create_instance()

if options == "delete":
    options_delete = Prompt.ask("Delete:", choices=["user", "security group", 'instance'])
    if options_delete == "instance":
        instance_name = Prompt.ask("[blue]Instance Name:[/blue]")
        delete_instance(instance_name)

    if options_delete == "security group":
        sg_name = Prompt.ask("[blue]Security Group Name:[/blue]")
        delete_sg(sg_name)

    if options_delete == "user":
        user_name = Prompt.ask("[blue]User Name:[/blue]")
        delete_user(user_name)

if options == "list":
    rprint("Running AWS configure. Please enter your AWS credentials and use us-east-1 for region.")
    os.system("aws configure")

    options_list = Prompt.ask("List:", choices=["users", "security groups", 'instances'])

    if options_list == "instances":
        os.system("aws ec2 describe-instances --region us-east-1")
    
    if options_list == "users":
        os.system("aws iam list-users --region us-east-1")
    
    if options_list == "security groups":
        os.system("aws ec2 describe-security-groups --region us-east-1")
        
        







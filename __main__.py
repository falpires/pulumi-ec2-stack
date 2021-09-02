"""An AWS Python Pulumi program"""

from typing import overload
import pulumi
import pulumi_aws as aws
import requests

my_ip = requests.get("http://jsonip.com").json()['ip']

current = aws.get_caller_identity()

sg = aws.ec2.SecurityGroup('web-sg',
    description="Enables HTTP Access",
    ingress=[
        {"protocol": "tcp", "from_port": 80, "to_port": 80, "cidr_blocks": [f"{my_ip}/32"]},
        {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr_blocks": [f"{my_ip}/32"]}
    ])

ubuntu = aws.ec2.get_ami_ids(filters=[aws.ec2.GetAmiIdsFilterArgs(
        name="name",
        values=["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"],
    ),
    aws.ec2.GetAmiIdsFilterArgs(
        name="virtualization-type",
        values=["hvm"]
    )],
    owners=["099720109477"])

server = aws.ec2.Instance('web-server',
    ami=ubuntu.ids[0],
    instance_type='t2.micro',
    vpc_security_group_ids=[sg.name])


pulumi.export('public_ip', server.public_ip)
pulumi.export('public_dns', server.public_dns)
pulumi.export("accountId", current.account_id)
pulumi.export("callerArn", current.arn)
pulumi.export("callerUser", current.user_id)
import boto3
import time

# pip install awscli boto3

class AWS_Utils:

    def __init__(self, key_name, machine_type, security_group, image_id):
        self.key_name = key_name
        self.machine_type = machine_type
        self.security_group = [security_group]
        self.image_id = image_id
        self.ec2 = boto3.resource('ec2', region_name='us-east-1')
        self.ec2_client = boto3.client('ec2', region_name='us-east-1')


    def create_instance(self, number):
        instances = self.ec2.create_instances(ImageId=self.image_id,
                                  InstanceType=self.machine_type,
                                  KeyName=self.key_name,
                                  SecurityGroupIds=self.security_group,
                                  MinCount=number,
                                  MaxCount=number)
        ids = [instance.id for instance in instances]
        time.sleep(60)
        ips = self.get_public_ips(ids)
        return ids, ips


    def get_public_ips(self, ids):
        instances = self.ec2.instances.filter()
        ips = list()
        for instance in instances:
            if instance.id in ids:
                ips.append(instance.public_ip_address)
        return ips


    def end_instances(self, ids):
        response = self.ec2_client.terminate_instances(InstanceIds=ids)

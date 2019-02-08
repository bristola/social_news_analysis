import boto3
import time

# pip install awscli boto3

class AWS_Utils:

    def __init__(self, key_name, machine_type, security_group, image_id):
        self.key_name = key_name
        self.machine_type = machine_type
        self.security_group = [security_group]
        self.image_id = image_id
        self.ec2 = boto3.resource('ec2', region_name='us-east-2')
        self.ec2_client = boto3.client('ec2', region_name='us-east-2')


    def create_instance(self, number):
        """
        Create the input number of ec2 machines based on configuration placed in
        constructor.
        """
        instances = self.ec2.create_instances(ImageId=self.image_id,
                                  InstanceType=self.machine_type,
                                  KeyName=self.key_name,
                                  SecurityGroupIds=self.security_group,
                                  MinCount=number,
                                  MaxCount=number)
        # Get list of ec2 ids
        ids = [instance.id for instance in instances]
        # Wait for instances to be provisioned
        time.sleep(60)
        # Get the public ids that are needed to connect
        ips = self.get_public_ips(ids)
        return ids, ips


    def get_public_ips(self, ids):
        """
        Gets all the ip addresses that are needed for connecting to the ec2
        machine. Use input ids to get the ip.
        """
        # Query instance information from ec2 resource
        instances = self.ec2.instances.filter()
        ips = list()
        for instance in instances:
            # Check if current instance is one that we created
            if instance.id in ids:
                ips.append(instance.public_ip_address)
        return ips


    def end_instances(self, ids):
        """
        Ends all ec2 instances that are input by id in the parameters.
        """
        response = self.ec2_client.terminate_instances(InstanceIds=ids)

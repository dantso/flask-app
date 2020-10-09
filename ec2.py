import boto3
import botocore
import paramiko
import time

def menu():
    region_name = "default"
    while True:
        print ('Choose from the following regions: ')
        print ('1. us-east-1')
        print ('2. us-east-2')
        print ('3. us-west-1')
        print ('4. us-west-2')
        print ('5. ca-central-1')
        region_num = input("Enter a number from [1-5]: ")
        if not 1 <= int(region_num) <= 5:
            print ('Please enter a valid number!')
        else:
            if region_num == '1':
                region_name = "us-east-1"
            elif region_num == '2':
                region_name = "us-east-2"
            elif region_num == '3':
                region_name = "us-west-1"
            elif region_num == '4':
                region_name = "us-west-2"
            elif region_num == '5':
                region_name = "ca-central-1"
            break

    key_name = input("Enter your key name: ")
    github_repo = input("Enter your github repository url: ")    
    
    return region_name, key_name, github_repo
    
def get_image_id (region_name):
    image_id = ""
    ec2 = boto3.resource('ec2', region_name=region_name)
    filters = [
        {'Name': 'owner-id', 'Values': ['137112412989']}, 
        {'Name':'description', 'Values':['Amazon Linux 2 AMI 2.0.20200917.0 x86_64 HVM gp2']}
    ]
    images = ec2.images.filter(Filters=filters).all()

    for image in images:
        image_id = image.id

    return image_id

def get_vpc_id(region_name):
    client = boto3.client('ec2',region_name=region_name)
    response = client.describe_vpcs(
    )
    resp = response['Vpcs']
    vpc_id = resp[0]['VpcId']

    return vpc_id

def create_security_group(vpc_id, region_name):

    ec2 = boto3.resource('ec2', region_name=region_name)
    sec_group = ec2.create_security_group(
        GroupName='flask_group', Description='flask_group', VpcId=vpc_id)
    sec_group.authorize_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=80,
        ToPort=80
    )
    sec_group.authorize_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22
    )
    sec_group.authorize_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=5000,
        ToPort=5000
    )

def get_security_group_id(region_name):
    client = boto3.client('ec2', region_name=region_name)
    response=client.describe_security_groups(
        Filters=[
            {'Name': 'group-name', 'Values': ['flask_group']}
        ],
    )

    if (response['SecurityGroups']):
        security_group_id = response['SecurityGroups'][0]['GroupId']
    else:
        security_group_id = ''

    return security_group_id


def create_ec2_insance(region_name, image_id, key_name, security_group_id):
    ec2 = boto3.resource('ec2', region_name=region_name)
    instance = ec2.create_instances(
        ImageId = image_id,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't2.micro',
        KeyName = key_name,
        SecurityGroupIds=[
            security_group_id
        ],
    )
    print (instance[0].id)
    instance[0].wait_until_running()           
    instance[0].reload()
    time.sleep(30)
    host_id = instance[0].public_ip_address
    return host_id

def launch_app(host_id, key_name, github_repo):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.load_system_host_keys()
    client.connect(hostname=host_id, username="ec2-user", key_filename='./key/'+key_name+'.pem')
    stdin, stdout, stderr = client.exec_command('sudo yum install git -y && git clone '+github_repo+' && sudo bash ~/flask-app/shell.sh')
    print (stdout.readlines())
    time.sleep(3)
    stdin, stdout, stderr = client.exec_command('sudo python ~/flask-app/app.py &')
    print (stdout.readlines())
    time.sleep(60)
    #client.close()

    print ("Finished")

def main():
    user_inputs = menu()
    region_name = user_inputs[0]
    key_name = user_inputs[1]
    github_repo = user_inputs[2]
    image_id = get_image_id(region_name)
    print (image_id)
    vpc_id = get_vpc_id(region_name)
    print (vpc_id)
    security_group_id = get_security_group_id(region_name)
    if (not security_group_id):
        create_security_group(vpc_id, region_name)
        security_group_id = get_security_group_id(region_name)
    host_id = create_ec2_insance(region_name, image_id, key_name, security_group_id)
    print (host_id)
    launch_app(host_id, key_name, github_repo)


if __name__ == "__main__":
    main()

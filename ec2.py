import boto3
import botocore
import paramiko
import time

ec2 = boto3.resource('ec2', region_name='us-east-1')
instance = ec2.create_instances(
    #change ImageId to your ImageId
    ImageId = 'ami-0c94855ba95c71c99',
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.micro',
    #change Keyname to your KeyName
    KeyName = 'Ansible',
    #change SecurityGroupIds to your SecurityGroupIds
    SecurityGroupIds=[
        'sg-0a946195e26dcdd80',
    ],
)
print (instance[0].id)
instance[0].wait_until_running()           
instance[0].reload()
print (instance[0].public_ip_address)
time.sleep(15)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.load_system_host_keys()
#change key_filename to the location where your key is stored
client.connect(hostname=instance[0].public_ip_address, username="ec2-user", key_filename='C:/Users/Sonu_2/Downloads/Ansible.pem')
#change git clone to your github repository url
stdin, stdout, stderr = client.exec_command('sudo yum install git -y && git clone https://github.com/dantso/flask-app.git && sudo bash ~/flask-app/shell.sh')
print (stdout.readlines())
time.sleep(3)
<<<<<<< HEAD
stdin, stdout, stderr = client.exec_command('python ~/flask-app/app.py &')
=======
stdin, stdout, stderr = client.exec_command('python ~/flaskApp/app.py &')
>>>>>>> 0d64b1f3805887b0dc461646c2f30b8c6c8ec4c6
print (stdout.readlines())
time.sleep(3)
#client.close()

print ("Finished")

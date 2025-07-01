import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='eu-west-2') #your default region - mine is London "eu-west-2"
    sns = boto3.client('sns')
    
    filters = [{'Name': 'tag:AutoManage', 'Values': ['True']}]
    response = ec2.describe_instances(Filters=filters)
    
    instances_to_stop = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
        if instance['State']['Name'] == 'running'
    ]
    
    if instances_to_stop:
        ec2.stop_instances(InstanceIds=instances_to_stop)
        message = f"EC2 Instances Stopped: {instances_to_stop}"
        sns.publish(
            TopicArn="arn:aws:sns:eu-west-2:<replace_with_AWS_account_number>:EC2StartStopNotify", #replace with your  aws account number and region
            Subject="EC2 Stop Notification",
            Message=message
        )
    else:
        print("No instances to stop.")

    return {'StoppedInstances': instances_to_stop}

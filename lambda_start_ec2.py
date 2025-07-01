import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='eu-west-2')
    sns = boto3.client('sns')
    
    filters = [{'Name': 'tag:AutoManage', 'Values': ['True']}]
    response = ec2.describe_instances(Filters=filters)
    
    instances_to_start = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
        if instance['State']['Name'] == 'stopped'
    ]
    
    if instances_to_start:
        ec2.start_instances(InstanceIds=instances_to_start)
        message = f"EC2 Instances Started: {instances_to_start}"
        sns.publish(
            TopicArn="arn:aws:sns:eu-west-2:<aws-account-number>:EC2StartStopNotify", #replace your aws account number
            Subject="EC2 Start Notification",
            Message=message
        )
    else:
        print("No instances to start.")

    return {'StartedInstances': instances_to_start}

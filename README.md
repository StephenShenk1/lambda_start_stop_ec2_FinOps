# AWS EC2 Start/Stop Automation with SNS Notifications

## Overview

This project demonstrates an automated AWS FinOps lab to **start** and **stop** EC2 instances based on tags using AWS Lambda functions. It integrates with **SNS** for notifications and uses **EventBridge** (CloudWatch Events) for scheduled triggers.

---

## Features

- Lambda function to start EC2 instances tagged `AutoManage=True` and send SNS notifications.
- Lambda function to stop EC2 instances tagged `AutoManage=True` and send SNS notifications.
- IAM roles with least privilege policies for Lambda functions.
- EventBridge rules to schedule start and stop operations.
- SNS topic for email or other endpoint notifications.
- Infrastructure cleanup instructions.
- Ready for reuse and easy deployment.

---

## Prerequisites

- AWS CLI configured with appropriate credentials.
- AWS account with permissions to create Lambda functions, IAM roles, SNS topics, and EventBridge rules.
- Python 3.7+ (for local testing).

---

## Lambda Functions

### 1. Start EC2 Instances

**lambda_start_ec2.py**

```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='eu-west-2')
    sns = boto3.client('sns')

    filters = [{
        'Name': 'tag:AutoManage',
        'Values': ['True']
    }]

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
            TopicArn="arn:aws:sns:eu-west-2:YOUR_ACCOUNT_ID:EC2StartStopNotify",
            Subject="EC2 Start Notification",
            Message=message
        )
        print(message)
    else:
        print("No instances to start.")

    return {
        'StartedInstances': instances_to_start
    }


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
**2. Stop EC2 Instance**s
lambda_stop_ec2.py


import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='eu-west-2')
    sns = boto3.client('sns')

    filters = [{
        'Name': 'tag:AutoManage',
        'Values': ['True']
    }]

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
            TopicArn="arn:aws:sns:eu-west-2:YOUR_ACCOUNT_ID:EC2StartStopNotify",
            Subject="EC2 Stop Notification",
            Message=message
        )
        print(message)
    else:
        print("No instances to stop.")

    return {
        'StoppedInstances': instances_to_stop
    }


,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

**IAM Role Policies**
Attach the following inline policy to your Lambda roles (replace "Resource": "*" with tighter ARNs if needed):

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish"
            ],
            "Resource": "arn:aws:sns:eu-west-2:YOUR_ACCOUNT_ID:EC2StartStopNotify"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
**SNS Setup**
Create an SNS topic (e.g., EC2StartStopNotify).

Subscribe your email or other endpoints.

Confirm subscription from your email.


**EventBridge (CloudWatch Events) Rules**
Schedule Lambda invocations using cron expressions.

Example to start instances at 7:00 AM UTC daily:

aws events put-rule --name StartEC2Daily --schedule-expression "cron(0 7 * * ? *)"
aws events put-targets --rule StartEC2Daily --targets "Id"="1","Arn"="arn:aws:lambda:eu-west-2:YOUR_ACCOUNT_ID:function:StartEC2Function"

Similarly, schedule stop at 7:00 PM UTC daily.

**Deployment Steps**
Create IAM roles with above policy and trust relationship for Lambda.

Deploy the two Lambda functions.

Set environment variables or update the SNS topic ARN in the code.

Create SNS topic and subscriptions.

Create EventBridge rules to schedule start and stop Lambda triggers.

Test Lambda manually using AWS Console or CLI.

Monitor CloudWatch logs for executions.

**Cleanup**
To delete resources after demo:

Remove EventBridge rules (aws events delete-rule).

Delete Lambda functions.

Delete IAM roles and policies.

Delete SNS topic.

**Testing**
Use AWS Lambda Console to create test events with any JSON payload (empty {} works).

Monitor CloudWatch logs for output.

Verify EC2 instance states in AWS EC2 console.

Check email or SNS endpoint for notification messages.

**License**
MIT License

**Contact**
Created by Stephen Shenk
Email: stephen@sodaka.com

Feel free to customize your region, account IDs, and resource names before deployment.

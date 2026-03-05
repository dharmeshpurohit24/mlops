import boto3
import json

sqs_client = boto3.client('sqs')

def send_sqs_message(queue_url, file_name):
    sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps({
            "file_name": file_name
        })
    )

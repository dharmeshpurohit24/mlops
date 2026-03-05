import json
import logging
from utils.sns_helper import send_sns_notification
from utils.sqs_helper import send_sqs_message

SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:683044966293:itt-bkt-file-upload.fifo'
SQS_QUEUE_URL = 'https://sqs.ap-south-1.amazonaws.com/683044966293/itt-file-processing'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")

    # Extract file name from S3 event
    file_name = event['Records'][0]['s3']['object']['key']

    # SNS notification
    send_sns_notification(
        SNS_TOPIC_ARN,
        f"File uploaded: {file_name}",
        "S3 Upload Notification"
    )

    # Send to SQS
    send_sqs_message(SQS_QUEUE_URL, file_name)

    return {
        'statusCode': 200,
        'body': 'Success'
    }

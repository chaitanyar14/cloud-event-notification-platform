import json
import boto3
import re
import os

sqs = boto3.client("sqs")

QUEUE_URL = os.environ["QUEUE_URL"]


def lambda_handler(event, context):

    print("Event received:", event)

    # Get request body from API Gateway
    body = event.get("body", "{}")

    # Convert body to JSON
    try:
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "Invalid JSON request body"
            })
        }

    # Validate required fields
    event_type = data.get("event")
    user_id = data.get("user_id")
    email = data.get("email")

    if not event_type:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Missing required field: event"
            })
        }

    if not user_id:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Missing required field: user_id"
            })
        }

    if not email:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Missing required field: email"
            })
        }

    # Basic email validation
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(email_pattern, email):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Invalid email address"
            })
        }

    # Send validated event to SQS
    try:

        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(data)
        )

        print("Message sent to SQS")
        print("Message ID:", response["MessageId"])

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Event received and queued successfully",
                "message_id": response["MessageId"]
            })
        }

    except Exception as e:

        print("Error sending message to SQS:", str(e))

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Failed to queue event"
            })
        }

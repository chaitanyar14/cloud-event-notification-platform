import json
import boto3
import os
from datetime import datetime, timezone

ses = boto3.client("ses", region_name="ap-south-1")
dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")

table = dynamodb.Table("notification-history")

SENDER = os.environ["SENDER_EMAIL"]


def lambda_handler(event, context):

    print("SQS message received")

    for record in event["Records"]:

        message_id = record["messageId"]
        body = record["body"]

        print("Message ID:", message_id)
        print("Raw message:", body)

        try:
            data = json.loads(body)

            event_type = data.get("event")
            user_id = data.get("user_id")
            email = data.get("email")

            print("Event:", event_type)
            print("User ID:", user_id)
            print("Email:", email)

            response = ses.send_email(
                Source=SENDER,
                Destination={
                    "ToAddresses": [email]
                },
                Message={
                    "Subject": {
                        "Data": f"Notification: {event_type}"
                    },
                    "Body": {
                        "Text": {
                            "Data": (
                                f"Hello {user_id},\n\n"
                                f"Your event '{event_type}' was received successfully.\n\n"
                                f"This notification was sent using Amazon SES."
                            )
                        }
                    }
                }
            )

            ses_message_id = response["MessageId"]

            print("SES Message ID:", ses_message_id)

            table.put_item(
                Item={
                    "event_id": message_id,
                    "event": event_type,
                    "user_id": user_id,
                    "email": email,
                    "status": "SENT",
                    "ses_message_id": ses_message_id,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )

            print("Notification history saved to DynamoDB")

        except json.JSONDecodeError:
            print("Message body is not valid JSON")
            raise

        except Exception as e:
            print("Error processing notification:", str(e))
            raise

    return {
        "statusCode": 200,
        "body": "Notification processed and history saved successfully"
    }

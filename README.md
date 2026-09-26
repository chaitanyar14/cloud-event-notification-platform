# Cloud-Based Event-Driven Notification & Automation Platform

An AWS serverless, event-driven notification platform that receives application events through an authenticated API, processes them asynchronously using Amazon SQS and AWS Lambda, sends email notifications using Amazon SES, and stores notification history in Amazon DynamoDB.

The project also includes automated CI/CD using GitHub Actions and GitHub OIDC for secure, keyless deployment to AWS.

---

## 🚀 Project Overview

Modern applications generate many events such as:

- `ORDER_PLACED`
- `ORDER_SHIPPED`
- `ORDER_DELIVERED`
- `PAYMENT_SUCCESS`
- `PAYMENT_FAILED`

Instead of processing these events synchronously, this platform uses an asynchronous event-driven architecture.

Applications send events to an API. The event is validated and placed into an Amazon SQS queue. A Lambda function processes the event, sends an email notification through Amazon SES, and stores the notification history in DynamoDB.

---

## 🏗️ Architecture

```text
                    Client / Application
                           |
                           | POST /events
                           v
                  +-------------------+
                  |    API Gateway    |
                  |   HTTP API + Auth |
                  +---------+---------+
                            |
                            v
                  +-------------------+
                  | Lambda Authorizer |
                  +---------+---------+
                            |
                            v
              +--------------------------+
              | notification-event-      |
              | handler Lambda           |
              | Validation + Queueing    |
              +------------+-------------+
                           |
                           v
                  +-------------------+
                  |   Amazon SQS      |
                  | notification-     |
                  | event-queue       |
                  +---------+---------+
                            |
                     Automatic Trigger
                            |
                            v
              +--------------------------+
              | notification-processor   |
              | Lambda                   |
              +------------+-------------+
                           |
                  +--------+--------+
                  |                 |
                  v                 v
             Amazon SES         DynamoDB
             Email             Notification
             Delivery           History

                  Amazon CloudWatch
                  Logs + Monitoring
                         |
                         v
                    Error Alarm

                  SQS Dead Letter Queue
                    Failed Messages


                  Developer
                      |
                      v
                GitHub Repository
                      |
                      v
                GitHub Actions
                      |
                      v
                  GitHub OIDC
                      |
                      v
                   AWS IAM
                      |
                      v
                Lambda Deployment





✨ Features
🔐 API authentication using AWS Lambda Authorizer
✅ Request validation
⚡ Asynchronous event processing
📬 Amazon SQS event queue
☠️ SQS Dead Letter Queue for failed messages
⚙️ AWS Lambda serverless processing
📧 Email notifications using Amazon SES
🗄️ Notification history using DynamoDB
📊 CloudWatch logs and monitoring
🚨 CloudWatch error alarm
🔄 GitHub Actions CI/CD
🔑 GitHub OIDC authentication
🛡️ IAM least-privilege permissions
🔒 No long-lived AWS access keys stored in GitHub


☁️ AWS Services Used
| AWS Service        | Purpose                                        |
| ------------------ | ---------------------------------------------- |
| Amazon API Gateway | Exposes the event ingestion API                |
| AWS Lambda         | Authorization, validation and event processing |
| Amazon SQS         | Asynchronous event queue                       |
| Amazon SQS DLQ     | Handles repeatedly failed messages             |
| Amazon SES         | Sends email notifications                      |
| Amazon DynamoDB    | Stores notification history                    |
| Amazon CloudWatch  | Logs, monitoring and alarms                    |
| Amazon SNS         | Sends CloudWatch alarm notifications           |
| AWS IAM            | Access control and security                    |
| GitHub Actions     | CI/CD automation                               |
| GitHub OIDC        | Secure GitHub-to-AWS authentication            |



🔄 Event Processing Flow
1.Client sends an event to POST /events.
2.Amazon API Gateway receives the request.
3.Lambda Authorizer validates the Bearer token.
4.Event Handler Lambda validates the request body.
5.The validated event is sent to Amazon SQS.
6.Amazon SQS triggers the Notification Processor Lambda.
7.Notification Processor processes the event.
8.Amazon SES sends an email notification.
9.Notification details are stored in DynamoDB.
10.CloudWatch records Lambda execution logs.
11.Failed messages are retried by SQS.
12.Messages that repeatedly fail are moved to the Dead Letter Queue.


📦 Example Event
{
  "event": "ORDER_PLACED",
  "user_id": "U1001",
  "email": "customer@example.com",
  "data": {
    "order_id": "ORD1001",
    "product": "Laptop",
    "amount": 49999
  }
}



🔐 API Authentication

The API uses an AWS Lambda Authorizer.

Requests must include a Bearer token:

POST /events
Content-Type: application/json
Authorization: Bearer <API_TOKEN>

Requests without a valid token are rejected by API Gateway.





🌐 API Endpoint
POST /events

Example request:

POST https://<api-id>.execute-api.<region>.amazonaws.com/events

Example response:

{
  "message": "Event received and queued successfully",
  "message_id": "example-message-id"
}

The message_id identifies the message placed into Amazon SQS.




⚙️ Lambda Functions
1. event-api-authorizer

Responsible for API authentication.

Responsibilities:

Reads the Authorization header
Validates the Bearer token
Allows or denies API access
2. notification-event-handler

Responsible for receiving and validating events.

Responsibilities:

Reads the API Gateway request
Parses the JSON body
Validates required fields
Performs basic email validation
Sends validated events to Amazon SQS
Returns the SQS message ID

Required fields:

event
user_id
email
3. notification-processor

Responsible for processing events from SQS.

Responsibilities:

Receives SQS messages
Extracts event information
Sends email notifications using Amazon SES
Stores notification history in DynamoDB
Logs processing information to CloudWatch



📬 Amazon SQS

The project uses Amazon SQS to decouple event ingestion from event processing.

Queue:

notification-event-queue

This provides:

Asynchronous processing
Message buffering
Automatic retry
Better fault tolerance
Decoupling between Lambda functions



☠️ Dead Letter Queue

A Dead Letter Queue is configured for failed messages.

Queue:

notification-event-dlq

The system allows a message to be processed up to 3 times.

If processing continues to fail, the message is moved to the DLQ for further investigation.




📧 Amazon SES

Amazon SES is used to send notification emails.

Example notification:

Subject: Notification: ORDER_PLACED

Hello U1001,

Your event 'ORDER_PLACED' was received successfully.

This notification was sent using Amazon SES.




🗄️ DynamoDB

Notification history is stored in:

notification-history

Primary key:

event_id

Example stored information:

event_id
event
user_id
email
status
ses_message_id
timestamp

Example:

{
  "event_id": "example-message-id",
  "event": "ORDER_PLACED",
  "user_id": "U1001",
  "email": "customer@example.com",
  "status": "SENT",
  "ses_message_id": "example-ses-message-id",
  "timestamp": "2026-09-26T07:30:53Z"
}




📊 Monitoring

Amazon CloudWatch is used for Lambda monitoring.

CloudWatch provides:

Lambda execution logs
Error monitoring
Troubleshooting information
Operational visibility

A CloudWatch alarm is configured to monitor errors from:

notification-processor

The alarm triggers when Lambda errors are detected.




🔄 CI/CD Pipeline

The project uses GitHub Actions to automatically deploy Lambda code to AWS.

Developer
    |
    | git push
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    v
GitHub OIDC
    |
    v
AWS IAM Role
    |
    v
Package Lambda Functions
    |
    +----------------------+
    |                      |
    v                      v
Authorizer            Event Handler
Lambda                Lambda
    |                      |
    +----------+-----------+
               |
               v
      Notification Processor
             Lambda

The workflow automatically deploys:

event-api-authorizer
notification-event-handler
notification-processor

whenever code is pushed to the main branch.




🔑 GitHub OIDC Security

GitHub Actions does not use permanent AWS access keys.

Instead:

GitHub Actions
      |
      v
GitHub OIDC Token
      |
      v
AWS STS
      |
      v
IAM Role
      |
      v
Temporary AWS Credentials

The IAM role is restricted to the specific GitHub repository and main branch.

This reduces the need to store long-lived AWS credentials in GitHub.




🛡️ IAM Security

The project follows the principle of least privilege.

The GitHub Actions deployment role is permitted to update only the required Lambda functions.

The deployment role does not have:

Administrator access
IAM management permissions
S3 access
DynamoDB access
SQS access
SES access

Lambda application roles separately provide the permissions required by the application.




📁 Repository Structure
cloud-event-notification-platform/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── lambdas/
│   ├── authorizer/
│   │   └── lambda_function.py
│   │
│   ├── event-handler/
│   │   └── lambda_function.py
│   │
│   └── notification-processor/
│       └── lambda_function.py
│
└── README.md




🧪 Testing

The complete event-processing pipeline has been tested successfully.

API Request                 ✅
API Authentication          ✅
Request Validation          ✅
SQS Queue                   ✅
SQS Message Processing     ✅
Lambda Processing           ✅
SES Email Delivery          ✅
Email Received              ✅
DynamoDB History            ✅
CloudWatch Logs             ✅
SQS Dead Letter Queue       ✅
GitHub Actions CI/CD        ✅
GitHub OIDC Authentication  ✅
🔧 Technologies
Programming
Python
AWS
AWS Lambda
Amazon API Gateway
Amazon SQS
Amazon SES
Amazon DynamoDB
Amazon CloudWatch
Amazon SNS
AWS IAM
AWS STS
DevOps
Git
GitHub
GitHub Actions
GitHub OIDC
Docker




🚀 Future Enhancements

Planned improvements include:

Notification status API
Notification history API
Support for multiple notification channels
Event-driven dashboard
Automated unit tests in CI/CD
Infrastructure as Code using Terraform
Additional CloudWatch metrics
Improved event retry and failure handling
Application/client SDK integration




👨‍💻 Project Objective

The objective of this project is to demonstrate practical experience with:

AWS serverless architecture
Event-driven system design
Asynchronous processing
AWS security and IAM
API authentication
Cloud monitoring
Fault tolerance
CI/CD automation
GitHub OIDC
Cloud application deployment



📌 Project Status

Status: Working / Deployed

The complete event-driven notification workflow has been deployed and tested on AWS.

API → Lambda → SQS → Lambda → SES
                         |
                         └──→ DynamoDB

GitHub → Actions → OIDC → IAM → L

# ☁️ Cloud-Based Event-Driven Notification Platform

A serverless, event-driven notification platform built on AWS that allows applications such as e-commerce, banking, SaaS, and other systems to send notification events through a secure HTTP API.

The platform processes events asynchronously, sends email notifications using Amazon SES, stores notification history in DynamoDB, handles failures using SQS Dead Letter Queue (DLQ), monitors errors with CloudWatch, and deploys Lambda functions automatically using GitHub Actions and GitHub OIDC.

---

## 🏗️ Architecture

![Cloud-Based Event-Driven Notification Platform](docs/architecture.png)

### Runtime Flow

```text
Postman / Client
      |
      | POST /events
      v
API Gateway (HTTP API)
      |
      v
Lambda Authorizer
      |
      v
Event Handler Lambda
      |
      | SendMessage
      v
Amazon SQS
      |
      | SQS Trigger
      v
Notification Processor Lambda
      |
      +-------> Amazon SES -------> Customer Email
      |
      +-------> DynamoDB ---------> Notification History

SQS
 |
 | After repeated failures
 v
Dead Letter Queue (DLQ)

Lambda
 |
 v
CloudWatch
 |
 v
CloudWatch Alarm
 |
 v
SNS Email Alert
```

### CI/CD Flow

```text
GitHub
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
Lambda Deployment
```

---

## 🎯 Key Features

- ⚡ Serverless event-driven architecture
- 🔐 API authentication using Lambda Authorizer
- 📩 Asynchronous processing using Amazon SQS
- 🔄 Automatic retry and Dead Letter Queue
- 📧 Email notifications using Amazon SES
- 💾 Notification history using DynamoDB
- 📊 CloudWatch monitoring and alarms
- 🚨 SNS email alerts
- 🔑 IAM least-privilege permissions
- 🚀 GitHub Actions CI/CD
- 🔐 GitHub OIDC authentication
- 🧪 API testing using Postman

---

## 🔄 How It Works

1. Client sends an event using `POST /events`.
2. API Gateway receives the request.
3. Lambda Authorizer validates the Bearer token.
4. Event Handler Lambda validates the request.
5. The event is placed into Amazon SQS.
6. SQS triggers the Notification Processor Lambda.
7. Processor Lambda sends an email through Amazon SES.
8. Notification details are stored in DynamoDB.
9. Failed messages are retried and eventually moved to the DLQ.
10. CloudWatch monitors Lambda errors and SNS sends alerts.

---

## 📡 API Example

### Endpoint

```text
POST https://3y4clraaxa.execute-api.ap-south-1.amazonaws.com/events
```

### Headers

```text
Authorization: Bearer <API_TOKEN>
Content-Type: application/json
```

### Request

```json
{
  "event": "ORDER_PLACED",
  "user_id": "U1001",
  "email": "customer@example.com"
}
```

### Successful Response

```json
{
  "message": "Event received and queued successfully",
  "message_id": "..."
}
```

The customer email is supplied dynamically by the application sending the event. Customers do not need to be manually added to the notification platform.

---

## 🔐 Security

- Lambda Authorizer protects the API endpoint.
- IAM policies provide restricted permissions to AWS services.
- Sensitive configuration is stored using Lambda environment variables.
- GitHub Actions uses OIDC instead of long-term AWS access keys.
- AWS IAM controls CI/CD deployment permissions.

---

## ⚙️ CI/CD

GitHub Actions automatically deploys the three Lambda functions:

```text
event-api-authorizer
notification-event-handler
notification-processor
```

Deployment flow:

```text
Git Push
   ↓
GitHub Actions
   ↓
GitHub OIDC
   ↓
AWS IAM Role
   ↓
Lambda Deployment
```

---

## 🧪 Testing

The system was tested using Postman with:

- Valid event requests
- Missing required fields
- Invalid email addresses
- Unauthorized requests
- Successful SQS processing
- SES email delivery
- DynamoDB notification history
- Intentional Lambda failure
- SQS retry and DLQ handling

---

## 📸 Project Screenshots

### API Gateway

![API Gateway](docs/01-api-gateway-route.png)

### Lambda Functions

![Lambda Functions](docs/02-lambda-functions.png)

### SQS Queue and DLQ

![SQS](docs/03-sqs-queues.png)

### DynamoDB Notification History

![DynamoDB](docs/04-dynamodb-history.png)

### Email Notification

![SES Email](docs/05-ses-email.png)

### CloudWatch Monitoring

![CloudWatch](docs/06-cloudwatch-alarm.png)

### GitHub Actions CI/CD

![GitHub Actions](docs/07-github-actions-ci-cd.png)

---

## 🛠️ AWS Services

| Service | Purpose |
|---|---|
| API Gateway | HTTP API |
| Lambda | Serverless processing |
| SQS | Event queue |
| SQS DLQ | Failed message handling |
| SES | Email notifications |
| DynamoDB | Notification history |
| CloudWatch | Logs, metrics and alarms |
| SNS | Alert notifications |
| IAM | Access control |
| STS / GitHub OIDC | Secure CI/CD authentication |

---

## 📁 Project Structure

```text
cloud-event-notification-platform/
│
├── .github/
│   └── workflows/
│       └── deploy.yaml
│
├── docs/
│   ├── architecture.png
│   ├── 01-api-gateway-route.png
│   ├── 02-lambda-functions.png
│   ├── 03-sqs-queues.png
│   ├── 04-dynamodb-history.png
│   ├── 05-ses-email.png
│   ├── 06-cloudwatch-alarm.png
│   └── 07-github-actions-ci-cd.png
│
├── lambdas/
│   ├── authorizer/
│   ├── event-handler/
│   └── notification-processor/
│
└── README.md
```

---

## 👨‍💻 Author

**Chaitanya Raut**  
B.E. Information Technology | Cloud & DevOps

**Technologies:** AWS • Python • Lambda • API Gateway • SQS • SES • DynamoDB • CloudWatch • IAM • GitHub Actions • GitHub OIDC • Docker • Git • Postman

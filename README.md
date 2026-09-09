# AWS Serverless AI-Powered Contact Form System

A production-ready, highly available, secure, and scalable serverless contact form system built using AWS native services.

---

## 📐 Architecture Diagram
![AWS Architecture Diagram](images/architecture.png)

---

## 📸 System Screenshots & AWS Console Proofs

### 1. Frontend & Edge Security (S3, CloudFront & Basic Auth)
| Public Contact Form | Basic Auth Protection | S3 Bucket Objects |
| :---: | :---: | :---: |
| ![Contact Form](images/contact-form.png) | ![Basic Auth Prompt](images/basic-auth.png) | ![S3 Hosting](images/s3-bucket.png) |

| CloudFront CDN Distribution | Protected Admin Dashboard |
| :---: | :---: |
| ![CloudFront](images/cloudfront.png) | ![Admin Panel](images/admin-dashboard.png) |



---

### 2. Backend Logic, AI Processing & Storage
| API Gateway REST Setup | Lambda Environment Variables |
| :---: | :---: |
| ![API Gateway](images/api-gateway.png) | ![Lambda Config](images/lambda-env.png) |

| DynamoDB Live Records | Amazon SNS Topics |
| :---: | :---: |
| ![DynamoDB Items](images/dynamodb.png) | ![SNS Topics](images/sns-topics.png) |

---

## 🏗️ Architecture Stack & Best Practices
- **Amazon S3:** Private Static Web Content Hosting protected via OAC.
- **Amazon CloudFront:** Global CDN for SSL/HTTPS acceleration & Edge Basic Auth via CloudFront Functions.
- **Amazon API Gateway:** Managed REST API endpoints, CORS handling, and Throttling controls.
- **AWS Lambda (Python 3.12):** Serverless backend compute executing business rules and AI SDK calls.
- **Amazon Comprehend:** Automated Natural Language Processing (NLP) for real-time sentiment analysis.
- **Amazon DynamoDB:** Fully managed NoSQL store with On-Demand capacity mode.
- **Amazon SNS:** Pub/Sub alert system sending prioritized email notifications based on sentiment analysis.

---

## 🚀 How to Run & Deploy
1. Upload static files (`index.html`, `admin.html`) to your private S3 Bucket.
2. Setup Amazon CloudFront Distribution linked via Origin Access Control (OAC).
3. Create Amazon DynamoDB Table `ContactFormMessages` with Primary Key `MessageId`.
4. Deploy AWS Lambda function with proper IAM roles to access Comprehend, DynamoDB, and SNS.
5. Create REST API on API Gateway and enable CORS before linking Lambda Proxy integration.
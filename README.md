# AWS Serverless AI-Powered Contact Form System

A production-ready, highly available, secure, and scalable serverless contact form system built using AWS native services.

---

## 📐 System Architecture
![AWS Architecture Diagram](image/arc.png)

---

## 📸 System Screenshots & AWS Console Proofs

### 1. Frontend & Edge Security (S3, CloudFront & Basic Auth)
| Public Contact Form | Basic Auth Protection | S3 Bucket Hosting |
| :---: | :---: | :---: |
| ![Contact Form](image/dash1.jpeg) | ![Basic Auth Prompt](image/admin%20pass.jpeg) | ![S3 Hosting](image/S3.jpeg) |

| CloudFront CDN Distribution | Protected Admin Dashboard |
| :---: | :---: |
| ![CloudFront](image/cloud%20foront.jpeg) | ![Admin Panel](image/admin.jpeg) |

---

### 2. Backend Logic, AI Processing & Storage
| API Gateway REST Setup | Lambda Environment Variables |
| :---: | :---: |
| ![API Gateway](image/api.jpeg) | ![Lambda Config](image/lam%20inv.jpeg) |

| DynamoDB Live Records | Amazon SNS Topics |
| :---: | :---: |
| ![DynamoDB Items](image/dynamo%20.jpeg) | ![SNS Topics](image/SNS.jpeg) |

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

## 🚀 Deployment Steps
1. Upload static files (`index.html`, `admin.html`) to your private S3 Bucket.
2. Setup Amazon CloudFront Distribution linked via Origin Access Control (OAC).
3. Create Amazon DynamoDB Table `ContactFormMessages` with Partition Key `MessageId`.
4. Deploy AWS Lambda function with proper IAM permissions to access Comprehend, DynamoDB, and SNS.
5. Create REST API on API Gateway and enable CORS before linking Lambda Proxy integration.
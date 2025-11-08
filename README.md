# Serverless News Summarizer (AWS Lambda + API Gateway + DynamoDB)

This repository contains two completed challenges implemented on **AWS**:

1. **Challenge 1 – Cloud Storage Integration (File Uploader)**
2. **Challenge 2 – Serverless Function (News Summarizer)**

Both projects are fully hosted and accessible via public endpoints.

---

## Live Demo
Invoke Url: https://drive.google.com/file/d/1RgNLBtwMLDi7K0pbxPZ-pp2Ye8u0Pjyu/view?usp=drive_link

## Hosted API
Invoke URL: https://t4dfupsqj6.execute-api.ap-south-1.amazonaws.com/summarize

## Production Deployment
Invoke URL:  http://news-summarizer-dashboard.s3-website.ap-south-1.amazonaws.com/

---

## Objective
### Challenge 1 – File Uploader
- Upload image/text files securely to S3  
- Validate file size & type  
- Return uploaded file link instantly

### Challenge 2 – Serverless News Summarizer
- Accept a news URL and return a summarized version  
- Cache results in DynamoDB to avoid repeated API calls  
- Provide a simple web-based UI to interact with the serverless function

---

### Architecture Overview
- **Frontend:** Simple HTML dashboard (index.html)  
- **Backend:** AWS Lambda function in Python  
- **Storage:** AWS S3 Bucket  
- **Integration:** AWS API Gateway

---

### Features
- File upload with validation (Challenge 1)  
- News summarization via Lambda (Challenge 2)  
- DynamoDB caching for repeated URLs  
- Public dashboard hosted on S3  

---

## Setup Steps
### 1. Clone the repository

git clone https://github.com/ayesha2124/Serverless-News-Summarizer
cd Serverless-News-Summarizer
2. Set Environment Variables
HF_API_KEY → HuggingFace API key

DYNAMO_TABLE → DynamoDB table name (news_summary_cache)

3. Deploy Lambda Function
Zip and upload lambda_function.py or deploy using AWS SAM/CloudFormation

Configure API Gateway POST /summarize endpoint

Enable CORS for frontend

4. Configure DynamoDB
Create table news_summary_cache

Partition key: url_hash (String)

5. Deploy Web Dashboard
Upload index.html to AWS S3 bucket configured for static website hosting

Access public dashboard using the bucket endpoint

6. Test Locally
bash
Copy code
curl -X POST https://<your-api-url>/summarize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/news-article"}'

---

## Folder Structure

NEWS-SUMMARIZER/
│
├── lambda_function.py
├── requirements.txt
├── README.md
├── function.zip
├── index.html
└── other folders...

---

## Workflows / Features
Feature	Purpose
Lambda Function	Handles incoming requests, fetches article, and calls summarization API
API Gateway	Provides RESTful endpoint for the frontend and external clients
DynamoDB Caching	Stores summaries of URLs to avoid repeated API calls
S3 Static Website	Hosts web dashboard for user-friendly interaction
HuggingFace API	Performs NLP-based summarization

---

## Reflection
Learned AWS Lambda integration with API Gateway

Managed DynamoDB caching for serverless functions

Solved CORS issues for frontend-backend communication

Implemented a full end-to-end serverless deployment

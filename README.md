# aws-cloud-resume-scanner
Serverless Resume Scanner using AWS Lambda, API Gateway, S3 and DynamoDB
# Cloud-Based Resume Scanner

# Overview
      Cloud-Based Resume Scanner is a serverless AWS application that automates resume screening by comparing candidate resumes against
      a target job role and calculating a skill match score.The application allows users to upload resumes through a web interface. 
      Resumes are stored in Amazon S3 using secure pre-signed URLs.AWS Lambda functions process the uploaded resumes, extract skills,
      calculate a match score, and store the results in Amazon DynamoDB.

# Features
  Resume upload through web interface
  Secure file upload using S3 Pre-Signed URLs
  Automated resume text extraction
  Skill matching against target job roles
  Resume scoring system
  Result storage in DynamoDB
  Logging and monitoring using CloudWatch
  Fully serverless architecture
  
# AWS Services Used
  Amazon S3
  AWS Lambda
  Amazon API Gateway
  Amazon DynamoDB
  AWS IAM
  Amazon CloudWatch
  
# Architecture Flow
User uploads a resume and selects a target job role.
Frontend requests a pre-signed upload URL.
API Gateway invokes generateurl.py.
Lambda generates a secure S3 pre-signed URL.
Resume is uploaded directly to Amazon S3.
S3 ObjectCreated event triggers resumescanner.py.
Lambda extracts text and identifies relevant skills.
Skill score is calculated based on the selected role.
Results are stored in DynamoDB.
CloudWatch captures logs and execution metrics.
Project Structure
# File Structure
```
cloud-resume-scanner/
│
├── frontend/
│   └── index.html
│
├── lambda/
│   ├── Resume_scanner.py
│   ├── Generate_url.py
│
├── requirements-layer.txt
│
├── architecture/
│   └── architecture.png
│
├── screenshots/
│   ├── frontend.png
│   ├── dynamodb.png
│   ├── cloudwatch.png
│
├── requirements.txt
├── README.md
```

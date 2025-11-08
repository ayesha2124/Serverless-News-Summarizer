#  Cloud Intern Assessment – Hands-On Projects

This repository contains two completed challenges implemented on **AWS**:

1. **Challenge 1 – Cloud Storage Integration (File Uploader)**
2. **Challenge 2 – Serverless Function (News Summarizer)**

Both projects are fully hosted and accessible via public endpoints.

---

##  Challenge 1 – Simple File Uploader with AWS S3

###  Objective
Build a web app that allows users to upload a file (image or text) and stores it securely in **Amazon S3**, returning a link to access the uploaded file.

---

###  Architecture Overview
- **Frontend:** Simple HTML upload form  
- **Backend:** Python (Flask API) deployed on AWS Lambda  
- **Storage:** AWS S3 Bucket  
- **Integration:** AWS API Gateway for endpoint

---

###  Features
- Upload image/text files  
- Validate file size & type  
- Store securely in S3  
- Return uploaded file link instantly  

---

###  Folder Structure
NEWS-SUMMARIZER/
│
├── lambda_function.py
├── requirements.txt
├── README.md
├── function.zip
├── typing_extensions.py
└── other folders...


##  Live Demo
 [Click here to watch the demo video](https://drive.google.com/your-demo-link-here)

##  Hosted API
Invoke URL: https://t4dfupsqj6.execute-api.ap-south-1.amazonaws.com/summarize

##  Reflection
This project helped me understand AWS Lambda integration with API Gateway and NLP summarization. The tricky part was configuring CORS and connecting the function with the endpoint.
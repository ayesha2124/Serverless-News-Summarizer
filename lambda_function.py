# import json
# import os
# import requests
# from bs4 import BeautifulSoup
# import hashlib
# import traceback
# import boto3

# # Optional DynamoDB table for caching
# DYNAMO_TABLE = os.getenv("DYNAMO_TABLE")  # e.g., "news_summary_cache"
# dynamodb = boto3.resource("dynamodb") if DYNAMO_TABLE else None
# table = dynamodb.Table(DYNAMO_TABLE) if dynamodb else None

# # Extract main article text from the page
# def extract_text_from_url(url):
#     try:
#         html = requests.get(url, timeout=10).text
#     except Exception as e:
#         raise Exception(f"Error fetching URL: {str(e)}")
    
#     soup = BeautifulSoup(html, "html.parser")
#     # Focus on <article> tag first
#     article = soup.find("article")
#     if not article:
#         article = soup.find("body")
    
#     for tag in article(["script", "style", "aside", "header", "footer", "nav"]):
#         tag.extract()
    
#     text = article.get_text(separator="\n", strip=True)
#     return text

# # Summarize text using HuggingFace API
# def summarize_text(text):
#     api_url = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
#     headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}
    
#     # Limit text for speed and reliability
#     payload = {"inputs": text[:1000]}
    
#     try:
#         r = requests.post(api_url, headers=headers, json=payload, timeout=60)
#         r.raise_for_status()
#         data = r.json()
#     except requests.exceptions.RequestException as e:
#         raise Exception(f"HuggingFace API request failed: {str(e)}")
#     except json.JSONDecodeError:
#         raise Exception(f"HuggingFace returned invalid JSON: {r.text}")
    
#     if isinstance(data, list) and "summary_text" in data[0]:
#         return data[0]["summary_text"]
#     raise Exception(f"HuggingFace returned unexpected format: {data}")

# # DynamoDB caching helpers
# def get_cache(url):
#     if not table:
#         return None
#     key = hashlib.sha256(url.encode()).hexdigest()
#     response = table.get_item(Key={"url_hash": key})
#     return response.get("Item", {}).get("summary")

# def set_cache(url, summary):
#     if not table:
#         return
#     key = hashlib.sha256(url.encode()).hexdigest()
#     table.put_item(Item={"url_hash": key, "summary": summary})

# # Lambda handler
# def lambda_handler(event, context):
#     try:
#         print("Event received:", event)
#         body_str = event.get("body")
#         if not body_str:
#             return {"statusCode": 400, "body": json.dumps({"error": "Missing body"})}
        
#         body = json.loads(body_str)
#         url = body.get("url")
#         if not url:
#             return {"statusCode": 400, "body": json.dumps({"error": "Missing URL"})}

#         # Check DynamoDB cache first
#         cached_summary = get_cache(url)
#         if cached_summary:
#             return {"statusCode": 200, "body": json.dumps({"summary": cached_summary, "cached": True})}

#         text = extract_text_from_url(url)
#         if not text:
#             return {"statusCode": 400, "body": json.dumps({"error": "Empty article text"})}

#         summary = summarize_text(text)

#         # Store summary in DynamoDB
#         set_cache(url, summary)

#         return {"statusCode": 200, "body": json.dumps({"summary": summary, "cached": False})}

#     except Exception as e:
#         traceback.print_exc()
#         return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
import json
import os
import requests
from bs4 import BeautifulSoup
import hashlib
import traceback
import boto3
import time  # added for TTL

# Optional DynamoDB table for caching
DYNAMO_TABLE = os.getenv("DYNAMO_TABLE")  # e.g., "news_summary_cache"
TTL_SECONDS = 60 * 60 * 24  # 24 hours TTL

dynamodb = boto3.resource("dynamodb") if DYNAMO_TABLE else None
table = dynamodb.Table(DYNAMO_TABLE) if dynamodb else None

# Extract main article text from the page
def extract_text_from_url(url):
    try:
        html = requests.get(url, timeout=10).text
    except Exception as e:
        raise Exception(f"Error fetching URL: {str(e)}")
    
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("article") or soup.find("body")
    
    for tag in article(["script", "style", "aside", "header", "footer", "nav"]):
        tag.extract()
    
    text = article.get_text(separator="\n", strip=True)
    return text

# Summarize text using HuggingFace API
def summarize_text(text):
    api_url = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}
    payload = {"inputs": text[:1000]}  # Limit text for speed
    
    try:
        r = requests.post(api_url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"HuggingFace API request failed: {str(e)}")
    except json.JSONDecodeError:
        raise Exception(f"HuggingFace returned invalid JSON: {r.text}")
    
    if isinstance(data, list) and "summary_text" in data[0]:
        return data[0]["summary_text"]
    raise Exception(f"HuggingFace returned unexpected format: {data}")

# DynamoDB caching helpers
def get_cache(url):
    if not table:
        return None
    key = hashlib.sha256(url.encode()).hexdigest()
    response = table.get_item(Key={"url_hash": key})
    return response.get("Item", {}).get("summary")

def set_cache(url, summary):
    if not table:
        return
    key = hashlib.sha256(url.encode()).hexdigest()
    expiry = int(time.time()) + TTL_SECONDS  # TTL added
    table.put_item(Item={
        "url_hash": key,
        "summary": summary,
        "expiry_time": expiry  # TTL attribute
    })

# Lambda handler
def lambda_handler(event, context):
    try:
        print("Event received:", event)
        body_str = event.get("body")
        if not body_str:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing body"})}
        
        body = json.loads(body_str)
        url = body.get("url")
        if not url:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing URL"})}

        # Check DynamoDB cache first
        cached_summary = get_cache(url)
        if cached_summary:
            return {"statusCode": 200, "body": json.dumps({"summary": cached_summary, "cached": True})}

        text = extract_text_from_url(url)
        if not text:
            return {"statusCode": 400, "body": json.dumps({"error": "Empty article text"})}

        summary = summarize_text(text)

        # Store summary in DynamoDB with TTL
        set_cache(url, summary)

        return {"statusCode": 200, "body": json.dumps({"summary": summary, "cached": False})}

    except Exception as e:
        traceback.print_exc()
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

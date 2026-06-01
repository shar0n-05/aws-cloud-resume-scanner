import json
import boto3
import urllib.parse
import uuid
from decimal import Decimal

JOB_ROLES = {
    "python_developer": ["python", "django", "flask", "api", "sql"],
    "data_scientist": ["python", "machine learning", "pandas", "numpy", "statistics"],
    "cloud_engineer": ["aws", "cloud", "docker", "kubernetes", "devops"]
}


def extract_skills(text):
    skills_db = [
        "python", "aws", "django", "flask",
        "machine learning", "pandas", "numpy",
        "sql", "docker", "kubernetes", "cloud"
    ]

    text = text.lower()
    found_skills = []

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


def calculate_score(candidate_skills, role):
    required_skills = JOB_ROLES.get(role, [])

    if not required_skills:
        return 0

    match_count = sum(1 for skill in required_skills if skill in candidate_skills)
    score = (match_count / len(required_skills)) * 100

    return round(score, 2)



s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")


table = dynamodb.Table("ResumeScores")


def lambda_handler(event, context):

    print(" Step 1: Lambda triggered")
    print("Event:", json.dumps(event))

   
    try:
        import pdfplumber
        print(" pdfplumber imported successfully")
    except Exception as e:
        print("IMPORT ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": "pdfplumber import failed"
        }

    try:
        
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(
            event['Records'][0]['s3']['object']['key']
        )

        print(f"Bucket: {bucket}, Key: {key}")

       
        response = s3.head_object(Bucket=bucket, Key=key)
        print("Metadata:", response.get('Metadata', {}))

        role = response['Metadata'].get('role', 'cloud_engineer')
        print("Selected Role:", role)

        download_path = "/tmp/" + key.split("/")[-1]
        s3.download_file(bucket, key, download_path)

        print(" Step 2: File downloaded")

     
        extracted_text = ""

        with pdfplumber.open(download_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() or ""

        print("Step 3: Text extracted")

       
        if len(extracted_text) > 300000:
            extracted_text = extracted_text[:300000]

       
        skills = extract_skills(extracted_text)
        print("Skills:", skills)

        
        score = calculate_score(skills, role)
        print(" Score:", score)

        
        applicant_name = key.split("/")[-1]

        
        table.put_item(
            Item={
                "applicant_name": applicant_name,  # Partition key
                "file_name": key,
                "resume_text": extracted_text,
                "skills": skills,
                "role": role,
                "score": Decimal(str(score))
            }
        )

        print("Step 4: Written to DynamoDB")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Resume processed successfully",
                "skills": skills,
                "score": score,
                "role": role
            })
        }

    except Exception as e:
        print(" ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": str(e)
        }
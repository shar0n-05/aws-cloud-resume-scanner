import json
import boto3
import uuid

s3 = boto3.client("s3")

BUCKET_NAME = "resume-scanner-free"

def lambda_handler(event, context):

    print("Event:", event)

  
    try:
        body = json.loads(event.get('body', '{}'))
    except:
        body = {}

    filename = body.get('filename', 'test.pdf')
    role = body.get('role', 'cloud_engineer')

    unique_filename = str(uuid.uuid4()) + "-" + filename

    try:
        upload_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': unique_filename,
                'Metadata': {
                    'role': role
                }
            },
            ExpiresIn=300
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "upload_url": upload_url
            })
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": str(e)
        }
import boto3
from botocore.exceptions import NoCredentialsError

# AWS S3 configuration
S3_BUCKET = "your-s3-bucket-name"
S3_REGION = "your-region"  # e.g., "us-east-1"

def upload_to_s3(file_path, bucket=S3_BUCKET, s3_file=None):
    s3 = boto3.client('s3')
    if s3_file is None:
        s3_file = file_path
    try:
        s3.upload_file(file_path, bucket, s3_file)
        # Generate a URL for the file (this may vary depending on bucket policy)
        url = f"https://{bucket}.s3.{S3_REGION}.amazonaws.com/{s3_file}"
        return url
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
    return None

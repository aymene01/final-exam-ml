import boto3
from botocore.config import Config
import os

def upload_to_minio(file_path, bucket_name, object_name):
    """Upload a file to MinIO S3 storage"""
    try:
        # Initialize MinIO client
        s3_client = boto3.client(
            's3',
            endpoint_url=os.environ.get('MINIO_ENDPOINT_URL', 'http://minio:9000'),
            aws_access_key_id=os.environ.get('MINIO_ACCESS_KEY', 'minioadmin'),
            aws_secret_access_key=os.environ.get('MINIO_SECRET_KEY', 'minioadmin'),
            config=Config(signature_version='s3v4'),
            region_name=os.environ.get('MINIO_REGION_NAME', 'us-east-1')
        )
        
        # Create bucket if it doesn't exist
        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except ClientError:
            s3_client.create_bucket(Bucket=bucket_name)
        except Exception as e:
            print(f"Error creating bucket: {e}")
            
        # Upload file
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Successfully uploaded {file_path} to {bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"Error uploading to MinIO: {e}")
        return False
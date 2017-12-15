import logging

import boto3
import botocore

from config import S3_BUCKET, S3_KEY, S3_SECRET, S3_LOCATION


logger = logging.getLogger(__name__)

s3_client = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)


def get_s3_file_public_url(filename):
    """
    Get public URL or return None if does not exist.
    """
    try:
        s3_client.head_object(Bucket=S3_BUCKET, Key=filename)
    except botocore.exceptions.ClientError as error:
        error_code = int(error.response['Error']['Code'])
        if error_code == 404:
            return None
        raise
    return '{}{}'.format(S3_LOCATION, filename)


def upload_mp4_video_to_s3(file_path, filename):
    try:
        s3_client.upload_file(file_path, S3_BUCKET, filename, ExtraArgs={
            'ACL': 'public-read',
            'ContentType': 'video/mp4'
        })
    except botocore.exceptions.ClientError:
        raise

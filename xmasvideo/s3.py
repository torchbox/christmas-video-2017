import logging

import botocore
import boto3
from flask import current_app as app, g


logger = logging.getLogger(__name__)


def s3():
    if getattr(g, 's3', None):
        return g.s3
    g.s3 = boto3.client(
       "s3",
       aws_access_key_id=app.config['S3_KEY'],
       aws_secret_access_key=app.config['S3_SECRET'],
    )
    return g.s3


def s3_resource():
    if getattr(g, 's3_resource', None):
        return g.s3_resource
    g.s3_resource = boto3.resource(
       "s3",
       aws_access_key_id=app.config['S3_KEY'],
       aws_secret_access_key=app.config['S3_SECRET'],
    )
    return g.s3_resource


def get_s3_file_public_url(filename):
    """
    Get public URL or return None if does not exist.
    """
    try:
        s3().head_object(Bucket=app.config['S3_BUCKET'], Key=filename)
    except botocore.exceptions.ClientError as error:
        error_code = int(error.response['Error']['Code'])
        if error_code == 404:
            return None
        app.logger.exception('Failed to obtain information about %s '
                             'from S3', filename)
        raise
    return '{}{}'.format(app.config['S3_LOCATION'], filename)


def upload_mp4_video_to_s3(file_path, filename):
    app.logger.info('Started upload of %s to S3', file_path)
    args = {
        'ACL': 'public-read',
        'ContentType': 'video/mp4',
    }
    try:
        s3().upload_file(file_path, app.config['S3_BUCKET'], filename,
                         ExtraArgs=args)
        app.logger.info('Uploaded %s to S3', file_path)
    except (boto3.exceptions.S3UploadFailedError,
            botocore.exceptions.ClientError):
        app.logger.exception('Failed upload of %s to S3', file_path)
        raise


def flush_videos_from_s3():
    app.logger.info('Started flushing videos from S3')
    s3_resource().Bucket(app.config['S3_BUCKET']).objects.delete()

import os


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY')
PORT = 5000

XMAS_IMAGE_FOLDER = os.path.join(ROOT_DIR, 'images')
XMAS_OUTPUT_FOLDER = '/tmp/xmas/videos'
XMAS_IMAGE_TXT_FILES_DIR = '/tmp/xmas/image_txt_files'
XMAS_AUDIO_FILE = os.path.join(ROOT_DIR, 'beatbox.wav')

CACHE_FLUSH_PASSWORD = os.environ.get('CACHE_FLUSH_PASSWORD')

S3_BUCKET = os.environ.get('S3_BUCKET')
S3_KEY = os.environ.get('S3_ACCESS_KEY')
S3_SECRET = os.environ.get('S3_SECRET')
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)


try:
    from .local_settings import *  # noqa
except ImportError:
    pass

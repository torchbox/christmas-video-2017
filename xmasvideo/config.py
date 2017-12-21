import os


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY')

XMAS_IMAGE_FOLDER = os.path.join(ROOT_DIR, 'images')
XMAS_OUTPUT_FOLDER = '/tmp/xmas/videos'
XMAS_IMAGE_TXT_FILES_DIR = '/tmp/xmas/image_txt_files'
XMAS_VIDEOS_IMAGES_DIR = '/tmp/xmas/videos_images'
XMAS_AUDIO_FILE = os.path.join(ROOT_DIR, 'beatbox.wav')
XMAS_MAX_IMAGES = 56

CACHE_FLUSH_PASSWORD = os.environ.get('CACHE_FLUSH_PASSWORD')

S3_BUCKET = os.environ.get('S3_BUCKET')
S3_KEY = os.environ.get('S3_ACCESS_KEY')
S3_SECRET = os.environ.get('S3_SECRET')
S3_LOCATION = 'https://{}.s3.amazonaws.com/'.format(S3_BUCKET)

ACRONYMS = [
    'CCA',
    'RCA',
    'CSP',
    'IETF',
    'WRAP',
    'OTF',
    'GOSH',
    'WFP',
]

try:
    from .local_settings import *  # noqa
except ImportError:
    pass

from functools import wraps
import os
import re
import shutil
import string
import subprocess

from flask import abort, current_app as app, request


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim='-'):
    """Generates ASCII-only slug without digits."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = ''.join([i for i in word if i in string.ascii_lowercase])
        if word:
            result.append(word)
    return str(delim.join(result))


def cache_flush_password_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not app.config['CACHE_FLUSH_PASSWORD']:
            abort(403)
        if request.form.get('password') != app.config['CACHE_FLUSH_PASSWORD']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def flush_tmp_app_directories():
    try:
        shutil.rmtree(app.config['XMAS_OUTPUT_FOLDER'])
    except FileNotFoundError:
        pass
    app.logger.info('Deleted %s and its contents',
                    app.config['XMAS_OUTPUT_FOLDER'])
    try:
        shutil.rmtree(app.config['XMAS_IMAGE_TXT_FILES_DIR'])
    except FileNotFoundError:
        pass
    app.logger.info('Deleted %s and its contents',
                    app.config['XMAS_IMAGE_TXT_FILES_DIR'])
    try:
        shutil.rmtree(app.config['XMAS_VIDEOS_IMAGES_DIR'])
    except FileNotFoundError:
        pass
    app.logger.info('Deleted %s and its contents',
                    app.config['XMAS_VIDEOS_IMAGES_DIR'])


def create_image_for_video(video_path, message):
    os.makedirs(app.config['XMAS_VIDEOS_IMAGES_DIR'], exist_ok=True)
    image_filename = '{}.jpg'.format(os.path.split(video_path)[1])
    image_path = os.path.join(app.config['XMAS_VIDEOS_IMAGES_DIR'],
                              image_filename)
    if os.path.isfile(image_path):
        app.logger.info('Skipping generating of %s image, exists', image_path)
    app.logger.info('Generating %s image', image_path)
    create_image_cmd = [
        'ffmpeg',
        '-y',
        '-loglevel',
        'fatal',
        '-ss',
        '0',
        '-i',
        video_path,
        '-vframes',
        '1',
        '-q:v',
        '2',
        image_path,
    ]
    subprocess.check_call(create_image_cmd)
    return image_path

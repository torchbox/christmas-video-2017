import os
import urllib

from flask import abort, Flask, redirect, render_template, request, url_for

from .convert import pick_images, images_to_video
from .s3 import (
    upload_mp4_video_to_s3,
    get_s3_file_public_url,
    flush_videos_from_s3,
    upload_jpeg_image_to_s3,
)
from .utils import (
    cache_flush_password_required,
    flush_tmp_app_directories,
    slugify,
    create_image_for_video,
)


app = Flask(__name__)
app.config.from_object("xmasvideo.config")


@app.route('/')
def index():
    context = {
        'message_max_length': app.config['XMAS_MAX_IMAGES'],
    }
    return render_template('hello.html', **context)


@app.route('/', methods=['POST'])
def create():
    message = request.form.get('message')
    sluggified_message = slugify(message)
    if not sluggified_message:
        return redirect(url_for('index'))
    images = pick_images(sluggified_message)
    video_path = images_to_video(sluggified_message, images)
    video_filename = os.path.split(video_path)[1]
    if not get_s3_file_public_url(video_filename):
        upload_mp4_video_to_s3(video_path, video_filename)
    else:
        app.logger.info('%s exists on S3, skipping upload.', video_filename)
    image_path = create_image_for_video(video_path, message)
    image_filename = os.path.split(image_path)[1]
    if not get_s3_file_public_url(image_filename):
        upload_jpeg_image_to_s3(image_path, image_filename)
    else:
        app.logger.info('%s exists on S3, skipping upload.', image_filename)
    video_url_params = {
        'message': urllib.parse.quote(message, safe=''),
    }
    return redirect(url_for('video', **video_url_params))


@app.route('/video/<message>/')
def video(message):
    unescaped_message = urllib.parse.unquote(message)
    name = '{}.mp4'.format(slugify(unescaped_message))
    s3_video_url = get_s3_file_public_url(name)
    s3_image_url = get_s3_file_public_url('{}.jpg'.format(name))
    if not s3_video_url:
        app.logger.info('%s does not exist on S3', name)
        abort(404)
    context = {
        'video_url': s3_video_url,
        'share_image': s3_image_url,
        'message': unescaped_message,
        'share_description': unescaped_message,
    }
    return render_template('video.html', **context)


@app.route('/flush-s3/', methods=['POST'])
@cache_flush_password_required
def flush_s3():
    flush_videos_from_s3()
    return 'Flushed S3 videos'


@app.route('/flush-tmp/', methods=['POST'])
@cache_flush_password_required
def delete_tmp():
    flush_tmp_app_directories()
    return 'Flushed tmp files'

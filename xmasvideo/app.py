import os

from flask import abort, Flask, redirect, render_template, request, url_for
from flask_headers import headers

from .convert import pick_images, images_to_video
from .grid_image import create_grid_image
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
    unslugify,
)


app = Flask(__name__)
app.config.from_object("xmasvideo.config")


def max_length():
    return app.config['XMAS_MAX_IMAGES'] - len('Merry Christmas XTORCHBOX')


@app.route('/')
@headers({'Cache-Control':'public, max-age=60'})
def index():
    context = {
        'message_max_length': max_length(),
    }
    return render_template('hello.html', **context)


@app.route('/', methods=['POST'])
def create():
    message = request.form.get('message')
    sluggified_message = slugify(message)
    if not sluggified_message or len(sluggified_message) > max_length():
        return redirect(url_for('index'))
    images = pick_images(sluggified_message)
    last_frame_image_path = create_grid_image(sluggified_message, images)
    sharing_image_path = create_grid_image(sluggified_message, images,
                                           landscape=True)
    video_path = images_to_video(
        sluggified_message,
        images,
        last_frame_image_path=last_frame_image_path,
    )
    video_filename = os.path.split(video_path)[1]
    if not get_s3_file_public_url(video_filename):
        upload_mp4_video_to_s3(video_path, video_filename)
    else:
        app.logger.info('%s exists on S3, skipping upload.', video_filename)
    sharing_image_filename = '{}.jpg'.format(video_filename)
    if not get_s3_file_public_url(sharing_image_filename):
        upload_jpeg_image_to_s3(sharing_image_path, sharing_image_filename)
    else:
        app.logger.info('%s exists on S3, skipping upload.',
                        sharing_image_filename)
    video_url_params = {
        'message': sluggified_message,
    }
    return redirect(url_for('video', **video_url_params))


@app.route('/video/<message>/')
@headers({'Cache-Control':'public, max-age=300'})
def video(message):
    if message.lower() != message:
        video_url_params = {
            'message': message.lower(),
        }
        return redirect(url_for('video', **video_url_params))
    name = '{}.mp4'.format(message)
    s3_video_url = get_s3_file_public_url(name)
    s3_image_url = get_s3_file_public_url('{}.jpg'.format(name))
    if not s3_video_url:
        app.logger.info('%s does not exist on S3', name)
        abort(404)
    title = 'Merry Christmas {} ❤️ Torchbox'.format(unslugify(message))
    context = {
        'video_url': s3_video_url,
        'share_image': s3_image_url,
        'message': title,
        'share_description': title,
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

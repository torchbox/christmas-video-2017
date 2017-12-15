import os

from flask import Flask, render_template, request, redirect

from .convert import pick_images, images_to_video_ffmeg
from .s3 import get_s3_file_public_url, upload_mp4_video_to_s3


app = Flask(__name__)
app.config.from_object("xmasvideo.config")


@app.route('/')
def index():
    return render_template('hello.html')


@app.route('/create', methods=['POST'])
def create():
    message = request.form.get('message')
    images = pick_images(message)
    video_path = images_to_video_ffmeg(message, images)
    video_filename = os.path.split(video_path)[1]
    upload_mp4_video_to_s3(video_path, video_filename)
    return render_template('thanks.html', message=message,
                           video=video_filename)


@app.route('/video/<name>')
def video(name):
    s3_video_url = get_s3_file_public_url(name)
    if not s3_video_url:
        raise RuntimeError("Can't load the file")
    return redirect(s3_video_url)

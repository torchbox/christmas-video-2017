from flask import Flask, render_template, request, send_from_directory
from convert import pick_images, images_to_video
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('hello.html') 

@app.route('/create', methods=['POST'])
def create():
    message = request.form.get('message')
    images = pick_images(message)
    video = images_to_video(message, images)
    return render_template('thanks.html', message=message, video=video)

@app.route('/video/<name>')
def video(name):
    return send_from_directory('/tmp/videos/', name)
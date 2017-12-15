# Torchbox Christmas Card Generator

## Run locally

```
pip install -f requirements.txt
export FLASK_APP=app.py
flask run
```

## Todo

 - [ ] convert these TODOs to issues
 - [ ] add letters to images
 - [ ] edit images for consistent lighting and scale
 - [ ] name letter holding images with letter and number, e.g. `a1.jpg`
 - [x] write `generate(message)` method which creates a video made from images for each letter in `message`
 - [x] append audio file to video. video must be same duration as audio file (~20 seconds)
 - [ ] store the video on s3, e.g. `happy-christmas-tomasz-heart-torchbox.mp4`
 - [ ] build web UI for card creation
 - [ ] build web UI for card viewing / sharing
 - [ ] database for tracking created videos, views and shares

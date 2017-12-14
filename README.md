# Torchbox Christmas Card Generator

## Dependencies

```
pip install -f requirements.txt
```

## Todo

 - [ ] add letters to images
 - [ ] edit images for consistent lighting and scale
 - [ ] name images with letter and name, e.g. `p-tomasz.jpg`
 - [ ] write `generate(message)` method which creates a video made from images for each letter in `message`
 - [ ] append audio file to video. video must be same duration as audio file (~20 seconds)
 - [ ] store the video on s3, e.g. `happy-christmas-tomasz-heart-torchbox.mp4`
 - [ ] build web UI for card creation
 - [ ] build web UI for card viewing / sharing
 - [ ] database for tracking created videos, views and shares

## Notes

Create a video from all images, using ffmpeg

```
cat images/*.jpg | ffmpeg -f image2pipe -r 4 -vcodec mjpeg -i - -vcodec libx264 out.mp4
```

Rotate video 90 degrees counter-clockwise

```
ffmpeg -i out.mp4 -vf "transpose=2" out2.mp4
```
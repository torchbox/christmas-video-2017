# Torchbox Christmas Card Generator

## Dependencies

```
pip install -f requirements.txt
```

## Todo

 - [ ] convert these TODOs to issues
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

Add audio to video (https://superuser.com/a/590210)

```
ffmpeg -i input.mp4 -i input.mp3 -c copy -map 0:v:0 -map 1:a:0 output.mp4
```

ffmpeg option: use Python to number the files, pass them to ffmpeg for conversion

Python option: use cv2, PIL etc. See http://blog.extramaster.net/2015/07/python-pil-to-mp4.html
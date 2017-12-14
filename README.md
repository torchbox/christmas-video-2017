# Torchbox Christmas Card Generator

## Dependencies

```
pip install -f requirements.txt
```

## Notes

Create a video from all images, using ffmpeg

```
cat images/*.jpg | ffmpeg -f image2pipe -r 4 -vcodec mjpeg -i - -vcodec libx264 out.mp4
```

Rotate video 90 degrees counter-clockwise

```
ffmpeg -i out.mp4 -vf "transpose=2" out2.mp4
```
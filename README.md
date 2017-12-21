# Torchbox Christmas Card Generator

## Requirements

* Python 3
* S3 storage for videos required

## Run locally

```bash
pip install -r requirements.txt
./run.py
```

Make sure images are rotated correctly, e.g. with

```bash
mogrify -alpha on -auto-orient *.jpg
```

## FE assets
To compile Sass please.
```bash
yarn  # to install dependencies, run it once
yarn scss:watch
```

## Todo

 - [x] convert these TODOs to issues
 - [x] add letters to images
 - [x] edit images for consistent lighting and scale
 - [x] name letter holding images with letter and number, e.g. `a1.jpg`
 - [x] write `generate(message)` method which creates a video made from images for each letter in `message`
 - [x] append audio file to video. video must be same duration as audio file (~20 seconds)
 - [x] store the video on s3, e.g. `happy-christmas-tomasz-heart-torchbox.mp4`
 - [x] build web UI for card creation
 - [x] build web UI for card viewing / sharing
 - [ ] ~~database for tracking created videos, views and shares~~

## Deployment notes

Please set the following environmental variables
 * `CACHE_FLUSH_PASSWORD` - password used to flush already created videos.
 * `S3_BUCKET`, `S3_ACCESS_KEY`, `S3_SECRET` - S3 storage variables


Add dokku to your git remote:
```bash
git remote add dokku dokku@dokku.torchbox.click:beatbox
```

Add port 80:
```bash
dokku proxy:ports-add beatbox http:80:5000
dokku config:set SECRET_KEY='your app secret key' S3_SECRET='' S3_ACCESS_KEY='' S3_BUCKET='' CACHE_FLUSH_PASSWORD=''
```

Add Nginx caching:
```bash
dokku plugin:install https://github.com/koalalorenzo/dokku-nginx-cache.git nginx-cache
dokku nginx-cache:enable beatbox
```

Flushing created videos
```bash
curl -X POST -d "password=your-password-here" https://beatbox.torchbox.com/flush-s3/
curl -X POST -d "password=your-password-here" https://beatbox.torchbox.com/flush-tmp/
```

Flushing the Nginx cache
```bash
dokku nginx-cache:clear
```
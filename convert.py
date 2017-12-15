import cv2
import os
import random

IMAGE_FOLDER = '/Users/tom/Documents/code/python/tbx-xmas-2017/christmas-video-2017/images'
OUTPUT_FOLDER = '/tmp/videos'
AUDIO_FILE = 'beatbox.mp3'
FRAMES_PER_SECOND = 3
MAX_IMAGES = 20

def pick_images(message):
    # return a list of images, starting with letter images that spell
    # out the message, ending with enough non-letter images to pad
    # to the required length
    plain_images = [img for img in os.listdir(IMAGE_FOLDER) if img.startswith("P")]
    message_images = []
    # pick letter images for the message
    for letter in message.lower():
        if letter == ' ':
            image = random.choice(plain_images)
            message_images.append(image)
            plain_images.remove(image)  # don't use the same random image twice
        else:
            # TODO count letter usage so we don't use the same person twice
            letter_image = letter + '1.jpg'
            message_images.append(letter_image)
    # add non-letter images
    selected_plain_images = []
    for i in range(0, MAX_IMAGES - len(message)):
        image = random.choice(plain_images)
        selected_plain_images.append(image)
        plain_images.remove(image)  
    return message_images + selected_plain_images


def images_to_video(message, images):
    message_slug = message.replace(' ', '-')
    silent_filename = message_slug + '-silent.mp4'
    final_filename = message_slug + '.mp4'
    silent_filepath = os.path.join(OUTPUT_FOLDER, silent_filename)
    final_filepath = os.path.join(OUTPUT_FOLDER, final_filename)
    
    if os.path.isfile(final_filepath):
        return final_filename  # don't bother making the file again

    frame = cv2.imread(os.path.join(IMAGE_FOLDER, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(silent_filepath, fourcc, FRAMES_PER_SECOND, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(IMAGE_FOLDER, image)))

    cv2.destroyAllWindows()
    video.release()

    os.system("ffmpeg -i %s -i %s -shortest %s" % (silent_filepath, AUDIO_FILE, final_filepath))
    os.remove(silent_filepath)

    # print os.path.abspath(final_filepath)
    
    return final_filename

def images_to_video_ffmeg(message, images):
    # ffmpeg -f concat -r 1/2 -i list.txt -crf 20 -vf fps=8,format=yuv420p video.mp4
    message_slug = message.replace(' ', '-')
    silent_filename = message_slug + '-silent.mp4'
    final_filename = message_slug + '.mp4'
    silent_filepath = os.path.join(OUTPUT_FOLDER, silent_filename)
    final_filepath = os.path.join(OUTPUT_FOLDER, final_filename)
    
    if os.path.isfile(final_filepath):
        return final_filename  # don't bother making the file again

    tmpfile = '/tmp/%s.txt' % message_slug
    tempfo = open(tmpfile, 'w+t')
    for image in images:
        tempfo.write("file '%s'\n" % os.path.join(IMAGE_FOLDER, image))
    tempfo.close()

    # -r is framerate, -crf is quality (lower is better)
    combine_cmd = "ffmpeg -f concat -r 3 -safe 0 -i %s -crf 15 -vf fps=8,format=yuv420p %s" % (tmpfile, silent_filepath)
    os.system(combine_cmd)
    os.system("ffmpeg -i %s -i %s -shortest %s" % (silent_filepath, AUDIO_FILE, final_filepath))
    os.remove(silent_filepath)
    
    return final_filename
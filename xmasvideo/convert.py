from collections import Counter
import os
import random
import re
import subprocess

from flask import current_app as app


FFMPEG_COMMON_ARGS = [
    '-loglevel',
    'fatal',
    '-y',
]
FRAMES_PER_SECOND = 3


def get_next_letter_image(letter, letter_images, letter_counter):
    options = [img for img in letter_images if img.startswith(letter)]
    if not options:
        return
    if letter_counter[letter] >= len(options):
        letter_counter[letter] = 1
        return options[0]
    letter_counter[letter] += 1
    return options[letter_counter[letter]-1]


def pick_images(message):
    # return a list of images, starting with letter images that spell
    # out the message, ending with enough non-letter images to pad
    # to the required length
    plain_image_pattern = re.compile(r'^P.*\.jpg$')
    images_list = os.listdir(app.config['XMAS_IMAGE_FOLDER'])
    plain_images = [img for img in images_list
                    if plain_image_pattern.match(img)]
    letter_pattern = re.compile(r'^[a-z][0-9]+\.jpg$')
    letter_images = [img for img in images_list if letter_pattern.match(img)]
    letter_images.sort()
    letter_counter = Counter()
    message_images = []
    # pick letter images for the message
    message = 'merry-christmas-{}-❤-torchbox'.format(message)
    for letter in message.lower():
        if letter == ' ':
            image = random.choice(plain_images)
            message_images.append(image)
            plain_images.remove(image)  # don't use the same random image twice
        elif letter == '❤':
            message_images.append('heart.jpg')
        else:
            letter_image = get_next_letter_image(letter, letter_images,
                                                 letter_counter)
            if not letter_image:
                # TODO: Implement logic for when there's no letter image
                continue
            message_images.append(letter_image)
    # add non-letter images
    selected_plain_images = []
    for i in range(0, app.config['XMAS_MAX_IMAGES'] - len(message_images)):
        try:
            image = random.choice(plain_images)
        except IndexError:
            # Recycle images if needed
            plain_images = selected_plain_images.copy()
            random.shuffle(plain_images)
        selected_plain_images.append(image)
        plain_images.remove(image)
    # Use lastframe.jpg
    if selected_plain_images:
        for index, plain_image in enumerate(reversed(selected_plain_images)):
            reverse_index = (index + 1) * -1
            # last 5 frames only
            if reverse_index == -5:
                break
            if len(selected_plain_images) >= reverse_index:
                selected_plain_images[reverse_index] = 'lastframe.jpg'
                continue
    return message_images + selected_plain_images


def images_to_video(message, images):
    os.makedirs(app.config['XMAS_OUTPUT_FOLDER'], exist_ok=True)
    os.makedirs(app.config['XMAS_IMAGE_TXT_FILES_DIR'], exist_ok=True)
    message_slug = message.replace(' ', '-')
    silent_filename = '{}-silent.mp4'.format(message_slug)
    final_filename = '{}.mp4'.format(message_slug)
    silent_filepath = os.path.join(
        app.config['XMAS_OUTPUT_FOLDER'],
        silent_filename
    )
    final_filepath = os.path.join(
        app.config['XMAS_OUTPUT_FOLDER'],
        final_filename
    )

    if os.path.isfile(final_filepath):
        app.logger.info('%s exists, skip rendering the file', final_filepath)
        return final_filepath

    images_txt_tmp_file = os.path.join(
        app.config['XMAS_IMAGE_TXT_FILES_DIR'],
        '{}.txt'.format(message_slug)
    )
    tempfo = open(images_txt_tmp_file, 'w+t')
    for image in images:
        image_path = os.path.join(app.config['XMAS_IMAGE_FOLDER'], image)
        # Double check if file exists, otherwise ffmpeg may fail.
        if not os.path.isfile(image_path):
            continue
        line = "file '{}'\n".format(image_path)
        tempfo.write(line)
    tempfo.close()

    # Combine images into the video
    combine_images_cmd = [
        'ffmpeg',
    ] + FFMPEG_COMMON_ARGS + [
        '-f',
        'concat',
        '-r',
        '{fps}'.format(fps=FRAMES_PER_SECOND),
        '-safe',
        '0',
        '-i',
        images_txt_tmp_file,
        '-vcodec',
        'libx264',
        '-preset',
        'ultrafast',
        '-movflags',
        '+faststart',
        '-crf',
        '15',
        '-vf',
        'format=yuv420p',
        silent_filepath,
    ]
    app.logger.info('about to run: %s', combine_images_cmd)
    subprocess.check_call(combine_images_cmd)

    # Mix video with audio
    audio_cmd = [
        'ffmpeg',
    ] + FFMPEG_COMMON_ARGS + [
        '-i',
        silent_filepath,
        '-i',
        app.config['XMAS_AUDIO_FILE'],
        '-shortest',
        '-strict',
        '-2',
        '-vcodec',
        'libx264',
        '-movflags',
        '+faststart',
        '-preset',
        'ultrafast',
        final_filepath,
    ]
    app.logger.info('About to run %s', repr(audio_cmd))
    subprocess.check_call(audio_cmd)

    # Delete silent video file
    os.remove(silent_filepath)

    return final_filepath

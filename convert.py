import cv2
import os
import random

IMAGE_FOLDER = 'images'
OUTPUT_FOLDER = 'videos'
FRAMES_PER_SECOND = 5


def pick_images(message):
    message_images = []
    # pick letter images for the message
    for letter in message.lower():
        # TODO count letter usage so we don't use the same person twice
        letter_image = letter + '1.jpg'
        message_images.append(letter_image)
    # add non-letter images
    plain_images = []
    images = [img for img in os.listdir(IMAGE_FOLDER) if img.startswith("P")]
    for i in range(0, 20):  # TODO calculate number of remaining letters
        image = random.choice(images)
        plain_images.append(image)
        images.remove(image)  # don't use the same random image twice
    return message_images + plain_images


def images_to_video(message, images):
    frame = cv2.imread(os.path.join(IMAGE_FOLDER, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output = os.path.join(OUTPUT_FOLDER, message + '.mp4')
    video = cv2.VideoWriter(output, fourcc, FRAMES_PER_SECOND, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(IMAGE_FOLDER, image)))

    cv2.destroyAllWindows()
    video.release()


message = 'steps'
images = pick_images(message)
images_to_video(message, images)

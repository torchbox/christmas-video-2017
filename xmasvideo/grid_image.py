import os

import PIL.Image
import PIL.ImageDraw

from flask import current_app as app

PORTRAIT_MODE_SIZE = 800, 1200
LANDSCAPE_MODE_SIZE = PORTRAIT_MODE_SIZE[1], PORTRAIT_MODE_SIZE[0]
PORTRAIT_GRID_SIZE = 8, 6
LANDSCAPE_GRID_SIZE = PORTRAIT_GRID_SIZE[1], PORTRAIT_GRID_SIZE[0]+1


def next_image_dimension(image_size, total_rows_and_columns, index):
    total_rows, total_columns = total_rows_and_columns
    width, height = image_size
    one_image_width = round(width / total_columns)
    one_image_height = round(height / total_rows)
    image_row_number = int(index / total_columns)
    image_column_number = index % total_columns
    image_offset_x = image_column_number * one_image_width
    image_offset_y = image_row_number * one_image_height
    return (
        (one_image_width, one_image_height),
        (image_offset_x, image_offset_y)
    )


def create_grid_image(name, images, landscape=False):
    os.makedirs(app.config['XMAS_VIDEOS_IMAGES_DIR'], exist_ok=True)
    orientation = 'landscape' if landscape else 'portrait'
    image_size = PORTRAIT_MODE_SIZE
    grid_size = PORTRAIT_GRID_SIZE
    if landscape:
        image_size = LANDSCAPE_MODE_SIZE
        grid_size = LANDSCAPE_GRID_SIZE
    filepath = os.path.join(app.config['XMAS_VIDEOS_IMAGES_DIR'],
                            '{}-{}.jpg'.format(name, orientation))
    im = PIL.Image.new('RGB', image_size)
    for number, image in enumerate(images):
        new_size, new_offset = next_image_dimension(im.size, grid_size, number)
        image = PIL.Image.open(os.path.join(app.config['XMAS_IMAGE_FOLDER'],
                               image))
        image = image.resize(new_size, PIL.Image.ANTIALIAS)
        im.paste(image, new_offset)
    im.save(filepath)
    return filepath

import math
import os

import PIL.Image
import PIL.ImageDraw

from willow.plugins.pillow import PillowImage

from flask import current_app as app

PORTRAIT_MODE_SIZE = 800, 1200
LANDSCAPE_MODE_SIZE = 1600, 800
PORTRAIT_GRID_SIZE = 8, 7
LANDSCAPE_GRID_SIZE = 5, 10


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
        image = fill_image(new_size, image)
        im.paste(image, new_offset)
    im.save(filepath)
    return filepath


## COPIED FROM WAGTAIL
def fill_image(final_image_size, pillow, crop_closeness=0):
    willow = PillowImage(pillow)
    width, height = final_image_size
    image_width, image_height = willow.get_size()
    focal_point = Rect(image_width / 2, image_height / 2, image_width / 2,
                       image_height / 2)

    # Get crop aspect ratio
    crop_aspect_ratio = width / height

    # Get crop max
    crop_max_scale = min(image_width, image_height * crop_aspect_ratio)
    crop_max_width = crop_max_scale
    crop_max_height = crop_max_scale / crop_aspect_ratio

    # Initialise crop width and height to max
    crop_width = crop_max_width
    crop_height = crop_max_height

    # Use crop closeness to zoom in
    if focal_point is not None:
        # Get crop min
        crop_min_scale = max(focal_point.width, focal_point.height * crop_aspect_ratio)
        crop_min_width = crop_min_scale
        crop_min_height = crop_min_scale / crop_aspect_ratio

        # Sometimes, the focal point may be bigger than the image...
        if not crop_min_scale >= crop_max_scale:
            # Calculate max crop closeness to prevent upscaling
            max_crop_closeness = max(
                1 - (width - crop_min_width) / (crop_max_width - crop_min_width),
                1 - (height - crop_min_height) / (crop_max_height - crop_min_height)
            )

            # Apply max crop closeness
            crop_closeness = min(crop_closeness, max_crop_closeness)

            if 1 >= crop_closeness >= 0:
                # Get crop width and height
                crop_width = crop_max_width + (crop_min_width - crop_max_width) * crop_closeness
                crop_height = crop_max_height + (crop_min_height - crop_max_height) * crop_closeness

    # Find focal point UV
    if focal_point is not None:
        fp_x, fp_y = focal_point.centroid
    else:
        # Fall back to positioning in the centre
        fp_x = image_width / 2
        fp_y = image_height / 2

    fp_u = fp_x / image_width
    fp_v = fp_y / image_height

    # Position crop box based on focal point UV
    crop_x = fp_x - (fp_u - 0.5) * crop_width
    crop_y = fp_y - (fp_v - 0.5) * crop_height

    # Convert crop box into rect
    rect = Rect.from_point(crop_x, crop_y, crop_width, crop_height)

    # Make sure the entire focal point is in the crop box
    if focal_point is not None:
        rect = rect.move_to_cover(focal_point)

    # Don't allow the crop box to go over the image boundary
    rect = rect.move_to_clamp(Rect(0, 0, image_width, image_height))

    # Crop!
    willow = willow.crop(rect.round())

    # Get scale for resizing
    # The scale should be the same for both the horizontal and
    # vertical axes
    aftercrop_width, aftercrop_height = willow.get_size()
    scale = width / aftercrop_width

    # Only resize if the image is too big
    if scale < 1.0:
        # Resize!
        willow = willow.resize((width, height))

    return willow.get_pillow_image()


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, key):
        return (self.x, self.y)[key]

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __repr__(self):
        return 'Vector(x: %d, y: %d)' % (
            self.x, self.y
)


class Rect:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def _get_size(self):
        return Vector(self.right - self.left, self.bottom - self.top)

    def _set_size(self, new_size):
        centroid = self.centroid
        self.left = centroid[0] - new_size[0] / 2
        self.right = centroid[0] + new_size[0] / 2
        self.top = centroid[1] - new_size[1] / 2
        self.bottom = centroid[1] + new_size[1] / 2

    size = property(_get_size, _set_size)

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.y

    def _get_centroid(self):
        return Vector((self.left + self.right) / 2, (self.top + self.bottom) / 2)

    def _set_centroid(self, new_centroid):
        size = self.size
        self.left = new_centroid[0] - size[0] / 2
        self.right = new_centroid[0] + size[0] / 2
        self.top = new_centroid[1] - size[1] / 2
        self.bottom = new_centroid[1] + size[1] / 2

    centroid = property(_get_centroid, _set_centroid)

    @property
    def x(self):
        return self.centroid.x

    @property
    def y(self):
        return self.centroid.y

    @property
    def centroid_x(self):
        # Included for backwards compatibility
        return self.centroid.x

    @property
    def centroid_y(self):
        # Included for backwards compatibility
        return self.centroid.y

    def as_tuple(self):
        # No longer needed, this class should behave like a tuple
        # Included for backwards compatibility
        return self.left, self.top, self.right, self.bottom

    def clone(self):
        return type(self)(self.left, self.top, self.right, self.bottom)

    def round(self):
        """
        Returns a new rect with all attributes rounded to integers
        """
        clone = self.clone()

        # Round down left and top
        clone.left = int(math.floor(clone.left))
        clone.top = int(math.floor(clone.top))

        # Round up right and bottom
        clone.right = int(math.ceil(clone.right))
        clone.bottom = int(math.ceil(clone.bottom))

        return clone

    def move_to_clamp(self, other):
        """
        Moves this rect so it is completely covered by the rect in "other" and
        returns a new Rect instance.
        """
        other = Rect(*other)
        clone = self.clone()

        if clone.left < other.left:
            clone.right -= clone.left - other.left
            clone.left = other.left

        if clone.top < other.top:
            clone.bottom -= clone.top - other.top
            clone.top = other.top

        if clone.right > other.right:
            clone.left -= clone.right - other.right
            clone.right = other.right

        if clone.bottom > other.bottom:
            clone.top -= clone.bottom - other.bottom
            clone.bottom = other.bottom

        return clone

    def move_to_cover(self, other):
        """
        Moves this rect so it completely covers the rect specified in the
        "other" parameter and returns a new Rect instance.
        """
        other = Rect(*other)
        clone = self.clone()

        if clone.left > other.left:
            clone.right -= clone.left - other.left
            clone.left = other.left

        if clone.top > other.top:
            clone.bottom -= clone.top - other.top
            clone.top = other.top

        if clone.right < other.right:
            clone.left += other.right - clone.right
            clone.right = other.right

        if clone.bottom < other.bottom:
            clone.top += other.bottom - clone.bottom
            clone.bottom = other.bottom

        return clone

    def __iter__(self):
        return iter((self.left, self.top, self.right, self.bottom))

    def __getitem__(self, key):
        return (self.left, self.top, self.right, self.bottom)[key]

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __repr__(self):
        return 'Rect(left: %d, top: %d, right: %d, bottom: %d)' % (
            self.left, self.top, self.right, self.bottom
        )

    @classmethod
    def from_point(cls, x, y, width, height):
        return cls(
            x - width / 2,
            y - height / 2,
            x + width / 2,
            y + height / 2,
        )

import numpy as np
import os
from skimage.transform import resize
from skimage import io

def clean_file_lst(file_name_lst, jpg=False):
    """
    Produces a list of files or subdirectories given a directory path.

    input:
    * file_name_lst: list of file/directory file names
    * jpg: True to return only jpg files

    output: cleaned list
    """
    if not jpg:
        return [fname for fname in file_name_lst if not fname.startswith('.')]
    elif jpg:
        return [fname for fname in file_name_lst if '.jpg' in fname]


def remove_borders(image):
    """
    Some of the shoe images have a faint grey border, affecting the
    composition of the background colors in later pre-processing steps. This
    function identifies any borders that exist in images and removes them,
    thereby shrinking the image's dimensions.

    input:
    * image

    output: resized image
    """

    # TO-DO
    return image


def resize_to_square(image, size, threshold=5):
    """
    Takes an image of a shoe, and resizes the shoe to fit within square
    dimensions, while maintaining the shoe's aspect ratio.

    input:
    * image (ndarray): the image file to be resized
    * size (integer): height/width of the resulting square image
    * threshold (integer): the higher the number, the more aggressive the
    cropping of the image

    output:
    * resized_image (ndarray)
    """

    # Phase 1: Crop the background to bound only the shoe.
    def is_threshold_exceeded(axis, index):
        if axis == 0:
            if (np.ptp(image[index,:,0]) > threshold or
                np.ptp(image[index,:,1]) > threshold or
                np.ptp(image[index,:,2]) > threshold):
                return True
            else:
                return False
        elif axis == 1:
            if (np.ptp(image[:,index,0]) > threshold or
                np.ptp(image[:,index,1]) > threshold or
                np.ptp(image[:,index,2]) > threshold):
                return True
            else:
                return False

    # Rows first
    for i in range(0, image.shape[0]):
        if is_threshold_exceeded(0, i):
            image = np.delete(image, np.s_[:i], 0)
            break

    for i in range(image.shape[0], -1, -1):
        if is_threshold_exceeded(0, i-1):
            image = np.delete(image, np.s_[i:], 0)
            break

    # Repeat for columns
    for i in range(0, image.shape[1]):
        if is_threshold_exceeded(1, i):
            image = np.delete(image, np.s_[:i], 1)
            break

    for i in range(image.shape[1], -1, -1):
        if is_threshold_exceeded(1, i-1):
            image = np.delete(image, np.s_[i:], 1)
            break


    # Phase 2: center the image, either horizontally or vertically
    def center_object(image, axis, large, small):
        new_image = image.copy()
        gap = int(round((large - small)/2.0))
        first_color = image[0,0]
        second_color = image[small-1,0] if axis == 0 else image[0,small-1]

        for i in range(0, gap):
            new_image = np.insert(new_image, 0, first_color, axis)

        for i in range(0, large - small - gap):
            new_image = np.insert(new_image,
                new_image.shape[axis]-1,
                second_color,
                axis)

        return new_image

    if (image.shape[0] > image.shape[1]):
        centered_image = center_object(image,
                            1,
                            image.shape[0],
                            image.shape[1])
    else:
        centered_image = center_object(image,
                            0,
                            image.shape[1],
                            image.shape[0])


    # Phase 3: resize the centered image to the desired square size
    resized_img = resize(centered_image, (size, size))
    return resized_img


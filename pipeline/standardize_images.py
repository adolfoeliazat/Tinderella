import os
from shared.preprocessing import clean_file_lst, resize_to_square
from skimage import io

HOME_PATH = '../'
IMAGES_DIRECTORY = os.path.join(HOME_PATH, 'images/')
OUTPUT_DIRECTORY = os.path.join(HOME_PATH, 'data/standardized_images')


def standardize_images(img_size):
    """
    Cleans up and standardizes images, ensuring all images are in proper
    directories.

    Input: Raw images in proper directories.
    Output: Standardized images in output directories
    (same directory structure)

    img_size: Size of the generated output square image. If dim
    is not provided, the number of channels is preserved.
    """

    # Iterate over each directory, keeping track of state, and save to
    # output directory
    if not os.path.exists(OUTPUT_DIRECTORY): os.mkdir(OUTPUT_DIRECTORY)

    # Resize and save images to output directories
    subdirectories = clean_file_lst(os.listdir(IMAGES_DIRECTORY), False)

    for subdir in subdirectories:
        subdir_path = os.path.join(IMAGES_DIRECTORY, subdir)
        new_subdir_path = os.path.join(OUTPUT_DIRECTORY, subdir)

        if not os.path.exists(new_subdir_path): os.mkdir(new_subdir_path)
        img_files = clean_file_lst(os.listdir(subdir_path), True)

        for img_file in img_files:
            # Reshape each image
            img_path = os.path.join(subdir_path, img_file)
            new_img_path = os.path.join(new_subdir_path, img_file)
            if os.path.exists(new_img_path): os.remove(new_img_path)

            print 'Processing', img_path
            resized_img = resize_to_square(io.imread(img_path), img_size)
            io.imsave(new_img_path, resized_img)
            print 'Saved', new_img_path


if __name__ == '__main__':
    """
    Move this all within one routine later if possible
    """
    standardize_images(200)

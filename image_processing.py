from __future__ import print_function, absolute_import
import os
import cv2
import helper
from PIL import Image


def _movie2imgs(file_path, to_dir, pic_num, n):
    """
    capture images from a movie
    arguments:
        file_path : path to video to extract images
        to_dir : directory path to save images
        pic_num : prefix of image file name such as class number
        n : image number
    return:
        n : last number of image to be used for continuous number
    """
    cap = cv2.VideoCapture(file_path)

    while(1):
        ret, frame = cap.read()
        if not ret:
            break

        try:
            filename = "{:02d}_{:04d}.png".format(pic_num, n)
            cv2.imwrite(os.path.join(to_dir, filename), frame)
        except:
            print('Image number {} in "{}" could not be captured.'.format(n, file_path))
        n += 1

    cap.release()

    return n


def movies2imgs(files, to_dir, img_prefix, init_number=0):
    """
    capture images from a movie
    arguments:
        files: paths of input movie files to extract image
        to_dir: directory path to save images
        img_prefix: prefix of image file name such as class number
        init_number: initial image number
            example)
                img_prefix=2, init_number=10
                saved data -> (to_dir)/02_0010.png, 02_0011.png ...
    """
    assert type(img_prefix) == int, "img_prefix should be integer"

    # create directory if necessary
    helper.mkdirs(to_dir)
    n = init_number     # image number

    for f in files:
        n = _movie2imgs(f, to_dir, img_prefix, n)

    print("Saved files to {}".format(to_dir))
    print("Total number of files are {}".format(n))


def image_crop(file_path, crop_position=0):
    """
    arguments:
        file_path : file path
        crop_position : image position to crop, range=[-1.0, 1.0]
            center : 0, left : -1, right : 1
    """
    im = Image.open(file_path)
    w, h = im.size
    d = w - h
    crop_position = (crop_position + 1.0) // 2.0
    p = int(d * crop_position)
    # set image size
    # if width is longer, crop horizontally
    if d > 0:
        crop_pos = (p, 0, p+h, h)
    # if height is longer, crop vertically
    elif d < 0:
        crop_pos = (0, -p, w, -p+w)

    im = im.crop(crop_pos)
    return im


def _make_path_name(file_path, to_dir):
    if to_dir:
        save_path = os.path.join(to_dir, os.path.basename(file_path))
    else:   # overwrite
        save_path = file_path
    return save_path


def _save_img(im, file_path, to_dir):
    """
    im : PIL.Image instance
    """
    save_path = _make_path_name(file_path, to_dir)
    im.save(save_path)


def _resize_img(img, img_size):
    img = img.resize((img_size, img_size))
    return img


def reshape_imgs(file_paths, to_dir=None, img_size=None, crop_position=0):
    """
    To square images
    arguments:
        file_paths : file paths
        to_dirs : if None, overwrite cropped image, if set path,
        img_size : integer, if not None, resize data to (img_size, img_size)
        crop_position : image position to crop, range=[-1.0, 1.0]
            center : 0, left : -1, right : 1
    """
    assert -1.0 < crop_position < 1.0, \
        "crop_position is out of range. (-1 < crop_position < 1)"

    if to_dir:
        helper.mkdirs(to_dir)

    for f in file_paths:
        im = image_crop(f, crop_position)
        if img_size:
            im = _resize_img(im, img_size)
        if im:
            _save_img(im, f, to_dir)
    print("Done")

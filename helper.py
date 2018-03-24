from __future__ import print_function
import os
import shutil
from glob import glob


def mkdirs(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def rmdirs(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)


def rename_files(dir, prefix, img_type="png"):
    paths = os.path.join(dir, '*.' + img_type)
    files = glob(paths)
    assert len(files) > 0, "No file is found."

    os.mkdir(os.path.join(dir, "renamed"))
    files = sorted(files)

    if type(prefix) == int:
        prefix = "{:02d}".format(prefix)

    for n, f in enumerate(files):
        os.rename(f, os.path.join(dir, "renamed", "{}_{:04d}.".format(prefix, n) + img_type))

    print("Total number of files : {}".format(n+1))

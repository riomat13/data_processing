import os
import shutil


def mkdirs(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def rmdirs(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)

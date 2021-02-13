#!/usr/bin/env python3

import glob
import logging
import os
import os.path

logger = logging.getLogger(__name__)


def get_imagefiles(imgpaths):
    imgs = []
    for imgpath in imgpaths:
        if "*" in imgpath:
            wildfiles = [
                i for i in (glob.iglob(imgpath, recursive=False)) if os.path.isfile(i)
            ]
            imgs.extend(wildfiles)
        elif os.path.isfile(imgpath) and not os.path.islink(imgpath):
            imgs.extend([imgpath])
        elif os.path.isdir(imgpath):
            with os.scandir(imgpath) as it:
                for entry in it:
                    if (
                        not entry.name.startswith("..")
                        and entry.is_file(follow_symlinks=False)
                    ):
                        imgs.extend([entry.path])
        else:
            raise ValueError("Unhandled image path: {0}".format(imgpath))

    imgs = filter_images(sorted(imgs))
    return imgs


def filter_images(imgs):
    img_ext = ["png", "jpg"]
    for img in imgs:
        if (os.path.splitext(img)[1][1:]).lower() not in img_ext:
            imgs.remove(img)
    return imgs

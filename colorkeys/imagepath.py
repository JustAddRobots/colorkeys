#!/usr/bin/env python3

import glob
import logging
import os
import os.path

from collections import Iterable

logger = logging.getLogger(__name__)


def gen_flat(list_):
    for i in list_:
        if isinstance(i, Iterable) and not isinstance(i, str):
            for x in gen_flat(i):
                yield x
        else:
            yield i


def get_imagefiles(imgpaths):
    imgpaths = list(gen_flat(imgpaths))
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
        if (os.path.splitext(img)[1].lstrip(".")).lower() not in img_ext:
            imgs.remove(img)
    return imgs

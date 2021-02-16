#!/usr/bin/env python3

import collections
import glob
import logging
import os
import os.path

logger = logging.getLogger(__name__)


def gen_flat(list_):
    """Create a flattened generator from list of nested iterables.

    This is useful, for nested lists of files.

    Args:
        list_ (list): Iterables to flatten.

    Yields:
        i (generator): Flattened iterator.
    """
    for i in list_:
        if isinstance(i, collections.Iterable) and not isinstance(i, str):
            for x in gen_flat(i):
                yield x
        else:
            yield i


def get_imagefiles(imgpaths):
    """Get image filenames from CLI arguments.

    Handles globbing of files and directories for quoted CLI arguments. Be aware
    the shell will automatically expand wildcard arguments without quotes.

    Args:
        imgpaths (list): Wildcards and or lists of files.

    Returns:
        imgs (list): Sorted and expanded file list.
    """
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

    imgs = sorted(filter_images(list(set(imgs))))
    return imgs


def filter_images(imgs):
    """Filter out image filenames based on extension.

    Args:
        imgs (list): Filenames.

    Returns:
        imgs (list): Image filenames.
    """
    img_ext = ["png", "jpg"]
    for img in imgs:
        if (os.path.splitext(img)[1].lstrip(".")).lower() not in img_ext:
            imgs.remove(img)
    return imgs

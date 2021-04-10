#!/usr/bin/env python3

# import glob
import itertools
import logging
# import os
# import os.path
from pathlib import Path

logger = logging.getLogger(__name__)


# def get_imagefiles(imgpaths):
#     """Get image filenames from CLI arguments.
#
#     Handles globbing of files and directories for quoted CLI arguments. Be aware
#     the shell will automatically expand wildcard arguments without quotes.
#
#     Args:
#         imgpaths (list): Wildcards and/or lists of files.
#
#     Returns:
#         imgs (set): Sorted and expanded file list.
#     """
#     imgpaths_itr = itertools.chain(imgpaths)
#     unglob_itr = [(unglob(i)) for i in imgpaths_itr]
#     itr = {i for i in itertools.chain.from_iterable(unglob_itr) if is_img(i)}
#     imgs = sorted(itr)
#     return imgs


def get_imagefiles(imgpaths):
    chn = itertools.chain(imgpaths)
    path_itrs = [unglob(i) for i in chn]
    img_set = {
        f"{p.parent}/{p.name}" for p in itertools.chain.from_iterable(path_itrs)
        if p.suffix in [".jpg", ".png"]
    }
    return sorted(img_set)


def unglob(imgpath):
    if isinstance(imgpath, list):
        imgpath = imgpath[0]
    p = Path(imgpath)
    if "*" in p.name:
        path_itr = p.parent.glob(p.name)
    elif p.is_dir():
        path_itr = p.iterdir()
    elif p.is_file():
        path_itr = [p]
    else:
        raise ValueError(f"Unhandled image path: {imgpath}")
    return path_itr


# def unglob(imgpath):
#     """Unglobs files and directories to an iterator containing filenames.
#
#     Args:
#         imgpath (str): Image path
#
#     Returns:
#         itr (iterator): iterator containing filenames of expanded path.
#
#     Raises:
#         ValueError: imagepath not file or wildcard.
#     """
#     if isinstance(imgpath, list) and len(imgpath) == 1:
#         imgpath = imgpath[0]
#
#     elif os.path.isfile(imgpath):
#         itr = [imgpath]
#     elif "*" in imgpath:
#         itr = [i for i in (glob.iglob(imgpath, recursive=False)) if os.path.isfile(i)]
#     elif os.path.isdir(imgpath):
#         with os.scandir(imgpath) as scan_itr:
#             itr = [i.path for i in scan_itr if (
#                 not i.name.startswith("..")
#                 and i.is_file(follow_symlinks=False)
#             )]
#     else:
#         raise ValueError(f"Unhandled image path: {imgpath}")
#
#     return itr
#
#
# def is_img(img):
#     """Determine whether a file is an image based on file extension.
#
#     Args:
#         img (str): Filename.
#
#     Returns:
#         is_img (bool): True if file has image extension.
#     """
#     img_ext = ["png", "jpg"]
#     is_img = os.path.splitext(img)[1].lstrip(".").lower() in img_ext
#     return is_img

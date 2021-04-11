#!/usr/bin/env python3

import itertools
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_imagefiles(imgpaths):
    """Get image filenames from CLI arguments.

    Handles globbing of files and directories for quoted CLI arguments. Be aware
    the shell will automatically expand wildcard arguments without quotes.

    Args:
        imgpaths (list): Wildcards, dirs, and/or lists of files.

    Returns:
        img_set (set): Sorted and expanded file list.
    """
    path_itrs = [unglob(i) for i in itertools.chain.from_iterable(imgpaths)]
    img_set = {
        f"{p.parent}/{p.name}" for p in itertools.chain.from_iterable(path_itrs)
        if p.suffix in [".jpg", ".png"]
    }
    return sorted(img_set)


def unglob(imgpath):
    """Unglobs files and directories to an iterator containing filenames.

    Args:
        imgpath (str): Image path

    Returns:
        itr (iterator): iterator containing filenames of expanded path.

    Raises:
        ValueError: image path does not exist.
        ValueError: image path not file or wildcard.
    """
    p = Path(imgpath)
    if "*" in p.name:
        path_itr = p.parent.glob(p.name)
    elif p.is_dir():
        path_itr = p.iterdir()
    elif p.is_file():
        path_itr = [p]
    elif not p.exists():
        raise ValueError(f"Non-existent path: {imgpath}, cwd: {Path.cwd()}")
    else:
        raise ValueError(f"Unhandled image path: {imgpath}, cwd: {Path.cwd()}")
    return path_itr

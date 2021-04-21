#!/usr/bin/env python3

import itertools
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_imagefiles(imgpaths):
    """Get image resource names from CLI arguments.

    Handles globbing of files and directories for quoted CLI arguments. Be aware
    the shell will automatically expand wildcard arguments without quotes.

    Args:
        imgpaths (list): Web URLs, Wildcards, dirs, and/or lists of files.

    Returns:
        imgs (list): Sorted and expanded file list.
    """
    urls = []
    paths = []
    for i in itertools.chain.from_iterable(imgpaths):
        if i.startswith(("http://", "https://")):
            urls.append(i)
        else:
            paths.append([i])
    path_itrs = [unglob(j) for j in itertools.chain.from_iterable(paths)]
    path_imgs = {
        f"{p.parent}/{p.name}" for p in itertools.chain.from_iterable(path_itrs)
        if p.suffix in [".jpg", ".png"]
    }
    imgs = path_imgs.union(set(urls))
    return sorted(imgs)


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

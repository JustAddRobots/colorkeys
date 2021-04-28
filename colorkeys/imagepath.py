#!/usr/bin/env python3

import boto3
import io
import itertools
import logging
import tarfile
import urllib
from pathlib import Path

from colorkeys.constants import _const as CONSTANTS
from colorkeys.createjson import get_timestamp
from engcommon import testvar

logger = logging.getLogger(__name__)


def get_imagefiles(imgpaths):
    """Get image resource names from CLI arguments.

    Handles globbing of files / directories for quoted CLI arguments, extracts
    tar image archives. Be aware the shell will automatically expand wildcard
    arguments without quotes.

    Args:
        imgpaths (list): Web URLs, wildcards, dirs, tar archives, and/or lists of files.

    eturns:
        imgs (list): Sorted and expanded file list.
    """
    urls = []
    tars = []
    paths = []
    for i in itertools.chain.from_iterable(imgpaths):
        if i.startswith(CONSTANTS().WEB_PREFIXES) and i.endswith(CONSTANTS().IMG_SUFFIXES):
            urls.append(i)
        elif i.endswith(CONSTANTS().TAR_SUFFIXES):
            tars.append([i])
        else:
            paths.append([i])

    path_unglob = [unglob(j) for j in itertools.chain.from_iterable(paths)]
    set_unglob = {
        f"{p.parent}/{p.name}" for p in itertools.chain.from_iterable(path_unglob)
        if p.suffix in [".jpg", ".png"]
    }
    path_untar = [untar(k) for k in itertools.chain.from_iterable(tars)]
    set_untar = {x for x in itertools.chain.from_iterable(path_untar)}
    imgs = set_unglob.union(
        set_untar.union(
            set(urls)
        )
    )
    return sorted(imgs)


def untar(filename, **kwargs):
    """Extract tar image archive and return imagepaths of included files.

    Args:
        filename (str): TAR filename, includes HTTP(S) and S3 endpoints.

    kwargs:
        dest_dir (str): Destination direct for extraction.
            Default is "/tmp/colorkeyes-[TIMESTAMP]"

    Returns:
        tar_images (list): Pathnames of extracted image files.
    """
    dest_dir = kwargs.setdefault("dest_dir", f"/tmp/colorkeys-{get_timestamp()}")
    if filename.startswith(CONSTANTS().WEB_PREFIXES):
        with urllib.request.urlopen(filename) as f:
            tf = tarfile.open(fileobj=io.BytesIO(f.read()))
    elif filename.startswith(CONSTANTS().S3_PREFIXES):
        p = Path(filename)
        my_bucket = p.parts[1]
        my_key = p.parts[2]
        s3 = boto3.resource("s3")
        obj = s3.Object(my_bucket, my_key)
        tf = tarfile.open(fileobj=io.BytesIO(obj.get()["Body"].read()))
    else:
        logger.debug(testvar.get_debug(filename))
        tf = tarfile.open(filename)
    tf.extractall(dest_dir)
    tar_imgs = [
        f"{dest_dir}/{i}" for i in tf.getnames()
        if i.endswith(CONSTANTS().IMG_SUFFIXES)
    ]
    return tar_imgs


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

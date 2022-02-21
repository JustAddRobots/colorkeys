#!/usr/bin/env python3

import boto3
import io
import itertools
import logging
import tarfile
import urllib
import zipfile

from hashlib import blake2b
from pathlib import Path
from random import random

from colorkeys.constants import _const as CONSTANTS
from colorkeys.codecjson import get_timestamp
from engcommon import testvar

logger = logging.getLogger(__name__)


def get_files(filepaths, suffixes):
    """Get file resource paths from CLI arguments.

    Handles globbing of files / directories for quoted CLI arguments, extracts
    archives files. Be aware the shell will automatically expand wildcard
    arguments without quotes.

    Args:
        filepaths (list): Web URLs, wildcards, dirs, zip/tar archives,
            and/or lists of files.

    Returns:
        files (list): Sorted and expanded file list.
    """
    urls = []
    arks = []
    paths = []
    for i in itertools.chain.from_iterable(filepaths):
        if i.startswith(CONSTANTS().WEB_PREFIXES) and i.endswith(suffixes):
            urls.append(i)
        elif i.endswith((CONSTANTS().TAR_SUFFIXES + CONSTANTS().ZIP_SUFFIXES)):
            arks.append([i])
        else:
            paths.append([i])

    path_unglob = [unglob(j) for j in itertools.chain.from_iterable(paths)]
    set_unglob = {
        f"{p.parent}/{p.name}" for p in itertools.chain.from_iterable(path_unglob)
        if p.suffix in suffixes
    }
    path_unark = [unark(k, suffixes) for k in itertools.chain.from_iterable(arks)]
    set_unark = {x for x in itertools.chain.from_iterable(path_unark)}
    files = set_unglob.union(
        set_unark.union(
            set(urls)
        )
    )
    logger.debug(files)
    return sorted(files)


def unark(filename, suffixes, **kwargs):
    """Extract archive and return paths of included target files.

    Args:
        filename (str): Archive filename, includes HTTP(S) and S3 endpoints.
        suffix (tuple): File extensions to target.

    Kwargs:
        dest_dir (str): Destination direct for extraction.
            Default is "/tmp/colorkeyes-unark-[TIMESTAMP]"

    Returns:
        extracted_paths (list): Pathnames of extracted files.
    """
    dest_dir = kwargs.setdefault(
        "dest_dir",
        f"/tmp/colorkeys-unark-{get_timestamp()}"
    )
    if filename.startswith(CONSTANTS().WEB_PREFIXES):
        with urllib.request.urlopen(filename) as f:
            if filename.endswith(CONSTANTS().TAR_SUFFIXES):
                cf = tarfile.open(fileobj=io.BytesIO(f.read()))
            elif filename.endswith(CONSTANTS().ZIP_SUFFIXES):
                cf = zipfile.ZipFile.open(fileobj=io.BytesIO(f.read()))
    elif filename.startswith(CONSTANTS().S3_PREFIXES):
        p = Path(filename)
        my_bucket = p.parts[1]
        my_key = p.parts[2]
        s3 = boto3.resource("s3")
        obj = s3.Object(my_bucket, my_key)
        if filename.endswith(CONSTANTS().TAR_SUFFIXES):
            cf = tarfile.open(
                fileobj=io.BytesIO(obj.get()["Body"].read())
            )
        elif filename.endswith(CONSTANTS().ZIP_SUFFIXES):
            cf = zipfile.ZipFile.open(
                fileobj=io.BytesIO(obj.get()["Body"].read())
            )
    else:
        logger.debug(testvar.get_debug(filename))
        if filename.endswith(CONSTANTS().TAR_SUFFIXES):
            cf = tarfile.open(filename)
        elif filename.endswith(CONSTANTS().ZIP_SUFFIXES):
            cf = zipfile.ZipFile(filename)
    cf.extractall(path=dest_dir)
    if filename.endswith(CONSTANTS().TAR_SUFFIXES):
        namelist = cf.getnames
    elif filename.endswith(CONSTANTS().ZIP_SUFFIXES):
        namelist = cf.namelist
    extracted_paths = [
        f"{dest_dir}/{i}" for i in namelist()
        if i.endswith(suffixes)
    ]
    return extracted_paths


def ark(obj_json, **kwargs):
    dest_dir = kwargs.setdefault(
        "dest_dir",
        f"/tmp/colorkeys-json-{get_timestamp()}"
    )
    k = str(random())
    random_basename = blake2b(k, digest_size=4).hexdigest()
    jsonfile = f"{random_basename}.json"
    jsonzip = f"{dest_dir}/{jsonfile}.zip"
    ramfile = io.StringIO()
    with zipfile.Zip(ramfile, mode='w') as zf:
        zf.writestr(jsonfile, obj_json)
    with open(jsonzip, "wb") as f:
        f.write(ramfile.getvalue())
    return None


def unglob(filepath):
    """Unglobs files and directories to an iterator containing filenames.

    Args:
        filepath (str): File path

    Returns:
        path_itr (iterator): iterator containing filenames of expanded path.

    Raises:
        ValueError: Path does not exist.
        ValueError: Path not file or wildcard.
    """
    p = Path(filepath)
    if "*" in p.name:
        path_itr = p.parent.glob(p.name)
    elif p.is_dir():
        path_itr = p.iterdir()
    elif p.is_file():
        path_itr = [p]
    elif not p.exists():
        raise ValueError(f"Non-existent path: {filepath}, cwd: {Path.cwd()}")
    else:
        raise ValueError(f"Unhandled path: {filepath}, cwd: {Path.cwd()}")
    return path_itr

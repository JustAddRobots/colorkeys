#!/usr/bin/env python3

import hashlib
import json
import logging
import pkg_resources
import psutil
import re
import sys
from datetime import datetime
from datetime import timezone
from decimal import Decimal
from pathlib import Path
from urllib import request

from engcommon import command
from engcommon import testvar

logger = logging.getLogger(__name__)


def compile(palette, epoch_seconds, **kwargs):
    """Prepare a ColorKey object for JSON encoding.

    This compiles a palette object with other relevant info into an object
    for JSON encoding.

    Args:
        palette (colorkeys.ColorKey): palette to prepare.
        epoch_seconds (str): Seconds used for non-AWS task_hash.

    kwargs:
        my_aws (aws.AWS): Instance including AWS container task info.

    Retuns:
        obj (dict): Palette ready for JSON encoding.
    """
    my_aws = kwargs.setdefault("my_aws", None)
    pkg_name = vars(sys.modules[__name__])["__package__"]
    histogram = {
        "algo": palette.hist.algo,
        "colorspace": palette.hist.colorspace,
        "n_clusters": palette.hist.num_clusters,
        "stopwatch": palette.hist.stopwatch,
        "hist_centroids": palette.hist.hist_centroids,
    }
    obj = {
        "filename": Path(palette.imgsrc).name,
        "filehash": get_filehash(palette.imgsrc),
        "shape": palette.img.shape,
        "timestamp": get_timestamp(),
        "version": get_version(pkg_name),
        "githash": get_githash(pkg_name),
        "histogram": histogram,
    }
    if my_aws:
        obj["cpu"] = my_aws.task_desc["cpu"]
        obj["memory"] = my_aws.task_desc["memory"]
        obj["task_hash"] = my_aws.task_hash
    else:
        obj["cpu"] = int(psutil.cpu_count(logical=False)) * 1024
        obj["memory"] = int(psutil.virtual_memory().available / 1024 / 1024)
        obj["task_hash"] = epoch_seconds
    return obj


def encode(obj):
    """Encode Python object to JSON."""
    return json.dumps(obj)


def decode(str_):
    """Decode Python object from JSON."""
    return json.loads(str_, parse_float=Decimal, parse_int=int)


def get_obj_from_file(filename):
    """Get Python object from JSON file."""
    with open(filename) as f:
        str_ = f.read()
    return decode(str_)


def get_version(pkg_name):
    """Get package version info."""
    return pkg_resources.get_distribution(pkg_name).version


def get_timestamp():
    """Get current timestamp."""
    timestamp = datetime.now(timezone.utc).astimezone().isoformat()
    return timestamp


def get_epoch_seconds():
    """Get the UNIX epoch in seconds."""
    ts = datetime.now(timezone.utc).astimezone().timestamp()
    epoch_seconds = str(ts).split('.')[0]
    return epoch_seconds


def get_githash(pkg_name):
    """Get the commit hash of a git package installed via PIP.

    pip packages installed via "git+http" needs "wheel" package installed
    to list git commit.

    Args:
        pkg_name (str): PIP package name.

    Returns:
        githash (str): Git commit hash.
    """
    dict_ = command.get_shell_cmd(f"python3 -m pip freeze | grep {pkg_name}")
    stdout = dict_["stdout"]
    regex = f"{pkg_name}.*@([0-9a-f]+)"
    match_0 = re.search(regex, stdout)
    testvar.check_null(match_0)
    githash = match_0.groups()[0]
    return githash


def get_filehash(filename):
    """Get hash of file.

    Args:
        filename (str): File name.

    Returns:
        filehash (str): hash digest of file.
    """
    BLOCK_SIZE = 65536
    filehash = hashlib.blake2b(digest_size=8)
    prefixes = ("http://", "https://")
    with request.urlopen(filename) \
            if filename.startswith(prefixes) else open(filename, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            filehash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return filehash.hexdigest()

#!/usr/bin/env python3

import datetime
import hashlib
import json
import logging
import pkg_resources
import re
import sys
from urllib import request

from engcommon import command
from engcommon import testvar

logger = logging.getLogger(__name__)


def compile(palette, **kwargs):
    """Prepare a ColorKey object for JSON encoding.

    This compiles a palette object with other relevant info into an object
    for JSON encoding.

    Args:
        palette (colorkeys.ColorKey): palette to prepare.

    kwargs:
        my_aws (aws.AWS): Instance including AWS container task info.

    Retuns:
        obj (dict): Palette ready for JSON encoding.
    """
    my_aws = kwargs.setdefault("my_aws", None)
    pkg_name = vars(sys.modules[__name__])["__package__"]
    hists = []
    for _, h in palette.hists.items():
        hists.append({
            "algo": h.algo,
            "colorspace": h.colorspace,
            "n_clusters": h.num_clusters,
            "stopwatch": h.stopwatch,
            "hist_centroids": h.hist_centroids,
        })
    obj = {
        "filename": palette.imgsrc,
        "sha1sum": get_sha1(palette.imgsrc),
        "shape": palette.img.shape,
        "timestamp": get_timestamp(),
        "version": get_version(pkg_name),
        "githash": get_githash(pkg_name),
        "histogram": hists,
    }
    if my_aws:
        obj["cpu"] = my_aws.task_desc["cpu"]
        obj["memory"] = my_aws.task_desc["memory"]
    return obj


def encode(obj):
    """Encode Python object to JSON."""
    return json.dumps(obj, indent=2)


def get_version(pkg_name):
    """Get package version info."""
    return pkg_resources.get_distribution(pkg_name).version


def get_timestamp():
    """Get current timestamp."""
    dt = datetime.datetime.now()
    timestamp = (
        f"{dt.year}.{dt.month:02d}.{dt.day:02d}-"
        f"{dt.hour:02d}{dt.minute:02d}{dt.second:02d}"
    )
    return timestamp


def get_githash(pkg_name):
    """Get the commit hash of a git package installed via PIP.

    pip packages installed via "git+http" needs "wheel" package installed
    to list git commit.

    Args:
        pkg_name (str): PIP package name.

    Returns:
        githash (str): Git commit hash.
    """
    d = command.get_shell_cmd(f"python3 -m pip freeze | grep {pkg_name}")
    stdout = d["stdout"]
    regex = f"{pkg_name}.*@([0-9a-f]+)"
    m = re.search(regex, stdout)
    testvar.check_null(m)
    githash = m.groups()[0]
    return githash


def get_sha1(filename):
    """Get SHA1 of file.

    Args:
        filename (str): File name.

    Returns:
        sha1sum (str): SHA1 checksum of file.
    """
    BLOCK_SIZE = 65536
    sha1sum = hashlib.sha1()
    prefixes = ("http://", "https://")
    with request.urlopen(filename) \
            if filename.startswith(prefixes) else open(filename, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            sha1sum.update(fb)
            fb = f.read(BLOCK_SIZE)
    return sha1sum.hexdigest()

#!/usr/bin/env python3

import datetime
import hashlib
import json
import pkg_resources
import re
import sys
from urllib import request

from engcommon import command
from engcommon import testvar


def encode(palettes):
    pkg_name = vars(sys.modules[__name__])["__package__"]
    obj = []
    for p in palettes:
        hists = []
        for _, h in p.hists.items():
            hists.append({
                "algo": h.algo,
                "colorspace": h.colorspace,
                "n_clusters": h.num_clusters,
                "hist_centroids": h.hist_centroids,
            })
        obj.append({
            "filename": p.imgsrc,
            "sha1sum": get_sha1(p.imgsrc),
            "timestamp": get_timestamp(),
            "version": get_version(pkg_name),
            "githash": get_githash(pkg_name),
            "histograms": hists,
        })
    return json.dumps(obj, indent=2)


def get_version(pkg_name):
    version = pkg_resources.get_distribution(pkg_name).version
    return version


def get_timestamp():
    dt = datetime.datetime.now()
    timestamp = (
        f"{dt.year}.{dt.month:02d}.{dt.day:02d}-"
        f"{dt.hour:02d}{dt.minute:02d}{dt.second:02d}"
    )
    return timestamp


def get_githash(pkg_name):
    d = command.get_shell_cmd(f"python3 -m pip freeze | grep {pkg_name}")
    stdout = d["stdout"]
    regex = f"{pkg_name}.*@([0-9a-f]+)"
    m = re.search(regex, stdout)
    testvar.check_null(m)
    githash = m.groups()[0]
    return githash


def get_sha1(fn):
    BLOCK_SIZE = 65536
    sha1sum = hashlib.sha1()
    with request.urlopen(fn) if fn.startswith(("http://", "https://")) else open(fn, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            sha1sum.update(fb)
            fb = f.read(BLOCK_SIZE)

#    with open(filename, "rb") as f:
#        fb = f.read(BLOCK_SIZE)
#        while len(fb) > 0:
#            sha1.update(fb)
#            fb = f.read(BLOCK_SIZE)
    return sha1sum.hexdigest()

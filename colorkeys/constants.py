#!/usr/bin/env python3

"""
Package constants.
"""


def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()
    return property(fget, fset)


class _const(object):

    @constant
    def DYNAMODB_URL_LOCAL():
        return "http://localhost:8000"

    @constant
    def S3_PREFIXES():
        return ("s3://", )

    @constant
    def WEB_PREFIXES():
        return ("http://", "https://")

    @constant
    def IMG_SUFFIXES():
        return (".jpg", ".png")

    @constant
    def TAR_SUFFIXES():
        return (".tar.bz2", ".tar.gz")

    @constant
    def ZIP_SUFFIXES():
        return (".zip", )

    @constant
    def JSON_SUFFIXES():
        return (".json", )

    @constant
    def DEFAULT_COLORSPACE():
        return "RGB"

    @constant
    def RESCALED_HEIGHT():
        return 400  # px

    @constant
    def HIST_BAR_HEIGHT():
        return 30  # px

    @constant
    def FIGURE_SIZE():
        return (8.00, 4.50)  # (x100) px

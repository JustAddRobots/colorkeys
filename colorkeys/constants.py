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
    def WEB_PREFIXES():
        return ("http://", "https://")

    @constant
    def IMG_SUFFIXES():
        return (".jpg", ".png")

    @constant
    def TAR_SUFFIXES():
        return (".tar.bz2", ".tar.gz")

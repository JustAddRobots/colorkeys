#!/usr/bin/env python3

from colorkeys import imagepath


def test_get_imagefiles_0(myimagepaths):
    assert imagepath.get_imagefiles([myimagepaths[0]]) == [
        "tests/fixture-01.jpg",
        "tests/fixture-01.png",
    ]


def test_get_imagefiles_1(myimagepaths):
    assert imagepath.get_imagefiles([myimagepaths[1]]) == [
        "tests/fixture-01.png",
    ]


def test_get_imagefiles_2(myimagepaths):
    assert imagepath.get_imagefiles([myimagepaths[2]]) == [
        "tests/fixture-01.jpg",
        "tests/fixture-01.png",
    ]


def test_get_imagefiles_3(myimagepaths):
    assert imagepath.get_imagefiles([myimagepaths[3]]) == [
        "tests/fixture-01.jpg",
    ]


def test_get_imagefiles(myimagepaths):
    assert imagepath.get_imagefiles(myimagepaths) == [
        "tests/fixture-01.jpg",
        "tests/fixture-01.png",
    ]


def test_get_imagefiles_shell_glob(myimagepaths_shell_glob):
    assert imagepath.get_imagefiles(myimagepaths_shell_glob) == [
        "tests/fixture-01.jpg",
        "tests/fixture-01.png",
    ]

#!/usr/bin/env python3

from colorkeys import filepath
from colorkeys.constants import _const as CONSTANTS


def test_get_files_0(myfilepaths):
    assert filepath.get_files(
        [myfilepaths[0]],
        CONSTANTS().IMG_SUFFIXES
    ) == [
        "tests/fixture-01.jpg",
        "tests/fixture-01.png",
    ]


def test_get_files_1(myfilepaths):
    assert filepath.get_files(
        [myfilepaths[1]],
        CONSTANTS().IMG_SUFFIXES
    ) == [
        "tests/fixture-01.png",
    ]


def test_get_files_2(myfilepaths):
    assert filepath.get_files(
        [myfilepaths[2]],
        CONSTANTS().IMG_SUFFIXES
    ) == [
        "tests/fixture-01.jpg",
        "tests/fixture-01.png",
    ]


def test_get_files_3(myfilepaths):
    assert filepath.get_files(
        [myfilepaths[3]],
        CONSTANTS().IMG_SUFFIXES
    ) == [
        "tests/fixture-01.jpg",
    ]


def test_get_files(myfilepaths):
    assert filepath.get_files(
        myfilepaths,
        CONSTANTS().IMG_SUFFIXES
    ) == [
        (
            "https://upload.wikimedia.org/wikipedia/"
            "commons/thumb/b/b4/Vincent_Willem_van_Gogh_128.jpg/"
            "192px-Vincent_Willem_van_Gogh_128.jpg"
        ),
        "tests/fixture-01.jpg",
        "tests/fixture-01.png",
    ]


def test_get_files_shell_glob(myfilepaths_shell_glob):
    assert filepath.get_files(
        myfilepaths_shell_glob,
        CONSTANTS().IMG_SUFFIXES
    ) == [
        "tests/fixture-01.jpg",
        "tests/fixture-01.png",
    ]

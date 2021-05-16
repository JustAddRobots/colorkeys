#!/usr/bin/python3


def test_get_command(myargs):
    assert myargs == {
        "algos": ["mbkmeans"],
        "aws": False,
        "colorspaces": ["RGB"],
        "debug": True,
        "debug_api": False,
        "images": [["tests/fixture-01.png"], ["tests/fixture-01.png"]],
        "json": False,
        "logid": None,
        "num_clusters": 5,
        "plot": False,
        "prefix": "/tmp/logs",
    }

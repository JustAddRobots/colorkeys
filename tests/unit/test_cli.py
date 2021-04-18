#!/usr/bin/python3


def test_get_command(myargs):
    assert myargs == {
        "algos": ["kmeans"],
        "colorspace": "RGB",
        "debug": True,
        "images": [["tests/fixture-01.png"], ["tests/fixture-01.png"]],
        "json": False,
        "logid": None,
        "num_clusters": 5,
        "plot": False,
        "prefix": "/tmp/logs",
    }

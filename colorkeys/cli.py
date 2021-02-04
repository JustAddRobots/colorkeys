#!/usr/bin/env python3

"""
This module is the CLI front-end for the colorkeys analysis tool.
"""

import argparse
import logging
import os
import pkg_resources
import sys

from colorkeys import ColorKey
from engcommon import clihelper
from engcommon import testvar


def get_command(args):
    """Get command args.
    Args:
        args (list): Argument list (e.g. sys.argv[1:]).

    Returns:
        args (dict): Arguments.
    """
    parser = argparse.ArgumentParser(
        description = "Colorkeys Palette Analysis Tool"
    )
    parser.add_argument(
        "-d", "--debug",
        action = "store_true",
        help = "print debug information",
    )
    parser.add_argument(
        "-a", "--algos",
        action = "store",
        choices = [
            "kmeans",
            "hac"
        ],
        default = [
            "kmeans",
            "hac"
        ],
        help = "set clustering algorithm",
    )
    parser.add_argument(
        "-i", "--image",
        action = "store",
        type = str,
        help = "set image",
        required = True
    )
    parser.add_argument(
        "-n", "--num_clusters",
        action = "store",
        type = int,
        help = "set number of cluster centroids",
        required = True
    )
    parser.add_argument(
        "-l", "--logid",
        action = "store",
        type = str,
        help = "set runtime log indentifier",
        required = False,
    )
    parser.add_argument(
        "-p", "--prefix",
        action = "store",
        type = str,
        default = "/tmp/logs",
        help = "set log directory prefix",
    )
    parser.add_argument(
        "-v", "--version",
        action = "version",
        version = pkg_resources.get_distribution(parser.prog).version
    )
    args = vars(parser.parse_args(args))
    return args


def run(args):
    """Run.
    Args:
        args (dict): CLI Arguments.

    Returns:
        None
    """
    # Standardised CLI bits
    project_name = (os.path.dirname(__file__).split("/")[-1])
    my_cli = clihelper.CLI(project_name, args)
    logger = my_cli.logger
    my_cli.print_versions()

    imgfile = args["image"]
    num_clusters = args["num_clusters"]
    algos = args["algos"]

    art = ColorKey(imgfile, num_clusters, algos)

    for algo, h in art.hists.items():
        logger.debug(testvar.get_debug(h.hist))

    art.show_palettes()

    return None


def main():
    args = sys.argv[1:]
    d = get_command(args)
    run(d)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Exceptions Found")
        logging.critical("Exiting.")
        sys.exit()

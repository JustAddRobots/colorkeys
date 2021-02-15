#!/usr/bin/env python3

"""
This module is the CLI front-end for the colorkeys analysis tool.
"""

import argparse
import logging
import os
import pkg_resources
import sys

from matplotlib import pyplot as plt
from time import time

from colorkeys.colorkeys import ColorKey
from colorkeys import imagepath
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
        help = "Print debug information",
    )
    parser.add_argument(
        "-a", "--algos",
        action = "store",
        choices = [
            "kmeans",
            # "hac"
        ],
        default = [
            "kmeans",
        ],
        help = "Set clustering algorithm",
    )
    parser.add_argument(
        "-c", "--colorspace",
        action = "store",
        choices = [
            "RGB",
        ],
        default = "RGB",
        help = "Set input image color space",
    )
    parser.add_argument(
        "-i", "--images",
        action = "append",
        type = str,
        nargs = "+",
        help = "set images",
        required = True
    )
    parser.add_argument(
        "-n", "--num_clusters",
        action = "store",
        type = int,
        help = "Set number of clusters to detect",
        required = True
    )
    parser.add_argument(
        "-l", "--logid",
        action = "store",
        type = str,
        help = "Set runtime log indentifier",
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
    # Standardised CLI bits.
    project_name = (os.path.dirname(__file__).split("/")[-1])
    my_cli = clihelper.CLI(project_name, args)
    logger = my_cli.logger
    my_cli.print_versions()

    # Get CLI args.
    imgpaths = args["images"]
    colorspace = args["colorspace"]
    num_clusters = args["num_clusters"]
    algos = args["algos"]

    imgfiles = imagepath.get_imagefiles(imgpaths)

    plt.show()
    for imgfile in imgfiles:
        time_start = time()
        art = ColorKey(imgfile, algos, num_clusters, colorspace=colorspace)
        time_end = time()
        time_duration = time_end - time_start

        logger.debug("file: {0}".format(os.path.basename(imgfile)))
        logger.debug("image shape: {0}".format(testvar.get_debug(art.img.shape)))
        logger.debug("render shape: {0}".format(testvar.get_debug(art.render.shape)))
        logger.debug("aspect ratio: {0:.2f}".format(art.aspect_ratio))
        logger.debug("time: {0:.2f}s".format(float(testvar.get_debug(time_duration))))
        for algo, h_dict in art.hists.items():
            for h_colorspace, h in h_dict.items():
                logger.debug("histogram, {0}: {1}".format(
                    h_colorspace,
                    testvar.get_debug(h.hist)
                ))
        art.show_palettes()
        plt.pause(0.001)
    input("\nPress [Return] to exit.")
    return None


def main():
    args = sys.argv[1:]
    d = get_command(args)
    run(d)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Exceptions Detected.")
        logging.critical("Exiting.")
        sys.exit()

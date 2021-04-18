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
from colorkeys import createjson
from colorkeys import imagepath
from engcommon import clihelper


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
            # "hac",  # HAC is too slow in sklearn
        ],
        default = [
            "kmeans",
        ],
        help = "Clustering algorithm",
        nargs = "+",
        type = str,
    )
    parser.add_argument(
        "-c", "--colorspace",
        action = "store",
        choices = [
            "RGB",
        ],
        default = "RGB",
        help = "Input image color space",
    )
    parser.add_argument(
        "-i", "--images",
        action = "append",
        help = "Images to process",
        nargs = "+",
        required = True,
        type = str,
    )
    parser.add_argument(
        "-j", "--json",
        action = "store_true",
        help = "Output as JSON",
    )
    parser.add_argument(
        "-l", "--logid",
        action = "store",
        help = "Runtime log indentifier",
        required = False,
        type = str,
    )
    parser.add_argument(
        "-n", "--num_clusters",
        action = "store",
        help = "number of clusters to detect",
        required = True,
        type = int,
    )
    parser.add_argument(
        "-p", "--prefix",
        action = "store",
        default = "/tmp/logs",
        help = "Log directory prefix",
        type = str,
    )
    parser.add_argument(
        "-t", "--plot",
        action = "store_true",
        help = "Plot color keys",
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
    showplot = args["plot"]
    showjson = args["json"]

    imgsrcs = imagepath.get_imagefiles(imgpaths)
    palettes = []

    for imgsrc in imgsrcs:
        time_start = time()
        palette = ColorKey(imgsrc, algos, num_clusters, colorspace=colorspace)
        time_end = time()
        time_duration = time_end - time_start
        logger.debug(f"file: {imgsrc}")
        logger.debug(f"time: {time_duration:.2f}s")

        palettes.append(palette)
        if showplot:
            plt.show()
            palette.show_palettes()
            plt.pause(0.001)

    if showplot:
        input("\nPress [Return] to exit.")

    palettes_json = createjson.encode(palettes)
    if showjson:
        print(palettes_json)

#    plt.show()
#    for imgsrc in imgsrcs:
#        time_start = time()
#
#        art = ColorKey(imgsrc, algos, num_clusters, colorspace=colorspace)
#
#        time_end = time()
#        time_duration = time_end - time_start
#
#        logger.debug(f"file: {imgsrc}")
#        logger.debug(f"image shape: {art.img.shape}")
#        logger.debug(f"render shape: {art.render.shape}")
#        logger.debug(f"aspect ratio: {art.aspect_ratio:.2f}")
#        logger.debug(f"time: {time_duration:.2f}s")
#
#        for _, h in art.hists.items():
#            logger.debug(
#                f"histogram, {h.algo} {h.colorspace}: "
#                f"{testvar.get_debug(h.hist_centroids)}"
#            )
#        art.show_palettes()
#        plt.pause(0.001)
#    input("\nPress [Return] to exit.")

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

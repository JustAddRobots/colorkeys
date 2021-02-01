#!/usr/bin/env python3

"""
This module is the CLI front-end for the standardised XHPL Stress Test.
"""

import argparse
import logging
import os
import pkg_resources
import sys

from colorkeys import kmeans
from engcommon import clihelper
from engcommon import formattext

def get_command(args):
    """Get command args.
    Args:
        args (list): Argument list (e.g. sys.argv[1:]).

    Returns:
        args (dict): Arguments.
    """
    parser = argparse.ArgumentParser(
        description = "XHPL Stress Test"
    )
    parser.add_argument(
        "-d", "--debug",
        action = "store_true",
        help = "print debug information",
    )
    parser.add_argument(
        "-i", "--image",
        action = "store",
        type = str,
        help = "set image",
    )
    parser.add_argument(
        "-k", "--kmeans",
        action = "store",
        type = int,
        help = "set number of cluster centroids",
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
    k = args["kmeans"]

    img = kmeans.get_img_rgb(imgfile)
    clust = kmeans.get_clusters(k, img)
    img_reshape = img.reshape(img.shape[0] * img.shape[1], img.shape[2])
    logger.debug(img_reshape.shape)

    clust.fit(img_reshape)
    hist = kmeans.get_cluster_histogram(clust)
    logger.debug(testvar.get_debug(hist))

    hist_bar = kmeans.get_hist_bar(hist, clust)
    kmeans.plot_hist_bar(img, hist_bar)

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


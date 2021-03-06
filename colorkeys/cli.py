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

from colorkeys.colorkeys import ColorKey
from colorkeys import aws
from colorkeys import createjson
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
        "-a", "--algos",
        action = "store",
        choices = [
            "kmeans",
            "mbkmeans",
            # "hac",  # HAC is too slow in sklearn
        ],
        default = [
            "mbkmeans",
        ],
        help = "Clustering algorithm(s) to use",
        nargs = "+",
        type = str,
    )
    parser.add_argument(
        "--aws",
        action = "store_true",
        default = False,
        help = "Access AWS resources for ECS task",
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
        "-d", "--debug",
        action = "store_true",
        help = "Print debug information",
    )
    parser.add_argument(
        "--debug-api",
        action = "store_true",
        help = "Print API debug information",
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
        help = "Number of clusters to detect",
        required = True,
        type = int,
    )
    parser.add_argument(
        "--prefix",
        action = "store",
        default = "/tmp/logs",
        help = "Log directory prefix",
        type = str,
    )
    parser.add_argument(
        "-p", "--plot",
        action = "store_true",
        help = "Plot color keys to display",
    )
    parser.add_argument(
        "-v", "--version",
        action = "version",
        version = pkg_resources.get_distribution(parser.prog).version,
        help = "Show version number and exit",
    )
    args = vars(parser.parse_args(args))
    return args


def set_API_logger(API, level):
    """Set the loglevel of dependent APIs.

    Args:
        API (str): API by Python module name.
        level (str): Log level.

    Returns:
        None
    """
    lgr = logging.getLogger(API)
    lgr.setLevel(eval(f"logging.{level}"))
    return None


def run(args):
    """Run.
    Args:
        args (dict): CLI Arguments.

    Returns:
        None
    """
    # Set API DEBUG loggers
    if args["debug_api"]:
        args["debug"] = True
        for API in ["matplotlib", "PIL"]:
            set_API_logger(API, "DEBUG")
    else:
        for API in ["matplotlib", "PIL"]:
            set_API_logger(API, "WARNING")

    # Standardised CLI bits.
    project_name = (os.path.dirname(__file__).split("/")[-1])
    my_cli = clihelper.CLI(project_name, args)
    logger = my_cli.logger
    logger_noformat = my_cli.logger_noformat
    my_cli.print_versions()

    # Get CLI args.
    imgpaths = args["images"]
    colorspace = args["colorspace"]
    num_clusters = args["num_clusters"]
    algos = args["algos"]
    showplot = args["plot"]
    showjson = args["json"]
    is_aws = args["aws"]

    # Get AWS info.
    if is_aws:
        my_aws = aws.AWS()
    else:
        my_aws = None

    imgsrcs = imagepath.get_imagefiles(imgpaths)
    if showplot:
        plt.show()
    objs = []
    for imgsrc in imgsrcs:
        palette = ColorKey(imgsrc, algos, num_clusters, colorspace=colorspace)
        obj = createjson.compile(palette, my_aws=my_aws)
        objs.append(obj)
        logger.debug(testvar.get_debug(obj))
        if showplot:
            palette.show_palettes()
            plt.pause(0.001)

    if showplot:
        input("\nPress [Return] to exit.")

    objs_json = createjson.encode(objs)
    if showjson:
        logger_noformat.info(objs_json)

    if is_aws:
        my_aws.upload_S3(objs_json)

    return None


def main():
    args = sys.argv[1:]
    d = get_command(args)
    try:
        run(d)
    except Exception:
        logging.exception("Exceptions Detected.")
        logging.critical("Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Exceptions Detected.")
        logging.critical("Exiting.")
        sys.exit(1)

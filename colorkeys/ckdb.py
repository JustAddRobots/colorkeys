#!/usr/bin/env python3

import argparse
import logging
import os
import pkg_resources
import sys

from engcommon import clihelper
from colorkeys import aws
from colorkeys import codecjson
from colorkeys import filepath
from colorkeys.constants import _const as CONSTANTS


def get_command(args):
    parser = argparse.ArgumentParser(
        description = "Colorkeys DynamoDB Tool"
    )
    parser.add_argument(
        "-d", "--debug",
        action = "store_true",
        help = "Print debug information",
    )
    parser.add_argument(
        "-l", "--logid",
        action = "store",
        help = "Runtime log indentifier",
        required = False,
        type = str,
    )
    parser.add_argument(
        "--prefix",
        action = "store",
        default = "/tmp/logs",
        help = "Log directory prefix",
        type = str,
    )
    parser.add_argument(
        "-s", "--site",
        action = "store",
        help = "DynamoDB site identifier",
        required = True,
        type = str,
        choices = ["local", "cloud"],
    )
    parser.add_argument(
        "-v", "--version",
        action = "version",
        version = pkg_resources.get_distribution("colorkeys").version,
        help = "Show version number and exit",
    )
    subparsers = parser.add_subparsers(
        help="Load Colorkeys sub-commands"
    )

    # subcommand "load"
    parser_load = subparsers.add_parser(
        "load",
        help = "Load JSON files",
    )
    parser_load.add_argument(
        "-f", "--files",
        action = "append",
        help = "File(s) to process",
        nargs = "+",
        required = True,
        type = str,
    )
    parser_load.set_defaults(func=load)

    # subcommand "query"
    parser_query = subparsers.add_parser(
        "query",
        help = "Query DB",
    )
    parser_query.add_argument(
        "-a", "--algo",
        action = "store",
        choices = [
            "kmeans",
            "mbkmeans",
            # "hac",  # HAC is too slow in sklearn
        ],
        help = "Clustering algorithm(s) for color detection",
        required = True,
        type = str,
    )
    parser_query.add_argument(
        "-c", "--colorspace",
        action = "store",
        choices = [
            "HSV",
            "RGB",
        ],
        help = "Colorspaces for color palette analysis",
        type = str,
    )
    parser_query.add_argument(
        "-i", "--images",
        action = "append",
        help = "Image(s) to process",
        nargs = "+",
        required = True,
        type = str,
    )
    parser_query.add_argument(
        "-n", "--num-clusters",
        action = "store",
        help = "Number of clusters to detect",
        required = True,
        type = int,
    )
    # parser_query.add_argument(
    #     "--stats",
    #     action = "store_true",
    #     help = "Generate statistics for query",
    # )
    parser_query.set_defaults(func=query)

    args = vars(parser.parse_args(args))
    return args


def run(args):
    # Get CLI args.
    project_name = (os.path.dirname(__file__).split("/")[-1])
    my_cli = clihelper.CLI(project_name, args)
    logger = my_cli.logger
    my_cli.print_versions()
    args["func"](args, logger)
    return None


def query(args, logger):
    imgpaths = args["images"]
    site = args["site"]
    algo = args["algo"]
    colorspace = args["colorspace"]
    num_clusters = args["num_clusters"]
    imgfiles = filepath.get_files(imgpaths, CONSTANTS().IMG_SUFFIXES)
    for filename in imgfiles:
        filehash = codecjson.get_filehash(filename)
        response = aws.query_dynamodb(
            site,
            "stage-colorkeys",
            filehash,
            algo,
            colorspace,
            num_clusters
        )
        logger.debug(response)
    return None


def load(args, logger):
    filepaths = args["files"]
    site = args["site"]
    jsonfiles = filepath.get_files(filepaths, CONSTANTS().JSON_SUFFIXES)
    for filename in jsonfiles:
        colorkeys = codecjson.get_obj_from_file(filename)
        aws.load_dynamodb(site, "stage-colorkeys", colorkeys)
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

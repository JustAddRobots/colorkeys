#!/usr/bin/env python3

import argparse
import logging
import numpy as np
import os
import pkg_resources
import sys

from pprint import pformat

from colorkeys import aws
from colorkeys import codecjson
from colorkeys import filepath
from colorkeys import statistics as colorstats
from colorkeys.constants import _const as CONSTANTS
from engcommon import clihelper
from engcommon import log


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
        "--debug-api",
        action = "store",
        help = "Print debug information for API",
        required = False,
        type = clihelper.csv_str,
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
        help = "JSON file(s) to load",
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
    xor_group = parser_query.add_mutually_exclusive_group(required=True)
    xor_group.add_argument(
        "--hash",
        action = "store",
        help = "Filehash(es) to process, separated by comma",
        type = clihelper.csv_str,
    )
    xor_group.add_argument(
        "-i", "--image",
        action = "append",
        help = "Image(s) to process",
        nargs = "+",
        type = str,
    )
    parser_query.add_argument(
        "-n", "--num-clusters",
        action = "store",
        help = "Number of clusters to detect",
        required = True,
        type = int,
    )
    parser_query.add_argument(
        "--stats",
        action = "store_true",
        help = "Generate statistics for query",
    )
    parser_query.set_defaults(func=query)

    args = vars(parser.parse_args(args))
    return args


def run(args):
    """Run.

    Args:
        args (dict): CLI Arguments.

    Returns:
        None
    """
    # Get CLI args.
    loglevels = {
        "boto3": "WARNING",
        "botocore": "WARNING",
        "urllib3": "WARNING",
    }
    if args["debug_api"]:
        args["debug"] = True
        loglevels = log.debug_enable(args["debug_api"], loglevels)

    log.set_loglevels(loglevels)
    project_name = (os.path.dirname(__file__).split("/")[-1])
    my_cli = clihelper.CLI(project_name, args)
    logger = my_cli.logger
    logger_noformat = my_cli.logger_noformat
    my_cli.print_versions()
    args["func"](args, logger, logger_noformat)
    return None


def query(args, logger, logger_noformat):
    site = args["site"]
    algo = args["algo"]
    colorspace = args["colorspace"]
    num_clusters = args["num_clusters"]
    stats = args["stats"]
    if args["image"]:
        imgpaths = args["image"]
        imgfiles = filepath.get_files(imgpaths, CONSTANTS().IMG_SUFFIXES)
        filehashes = []
        for filename in imgfiles:
            filehashes.append(codecjson.get_filehash(filename))
    elif args["hash"]:
        filehashes = args["hash"]
    colorkeys = []
    for filehash in filehashes:
        response = aws.query_dynamodb(
            site,
            "stage-colorkeys",
            filehash,
            algo,
            colorspace,
            num_clusters
        )
        colorkeys.extend(response["Items"])
    colorkeys = aws.replace_decimals(colorkeys)
    if stats:
        np.set_printoptions(precision=3, suppress=True)
        centroids = colorstats.get_centroids(colorkeys)
        clusters = colorstats.get_centroids_by_cluster(centroids)
        cluster_means = colorstats.get_cluster_means(clusters)
        cluster_stds = colorstats.get_cluster_stds(clusters)

        logger_noformat.debug(f"centroids:\n{pformat(centroids)}")
        logger_noformat.debug(f"clusters:\n{pformat(clusters)}")
        logger_noformat.info(f"means:\n{pformat(cluster_means)}")
        logger_noformat.info(f"stds:\n{pformat(cluster_stds)}")
    return None


def load(args, logger, logger_noformat):
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

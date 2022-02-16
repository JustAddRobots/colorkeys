#!/usr/bin/env python3

import argparse
import boto3
import json
import logging
import os
import pkg_resources
import sys

from colorkeys import clihelper
from colorkeys import filepath
from colorkeys.constants import _const as CONSTANTS


def get_command(args):
    parser = argparse.ArgumentParser(
        description = "Colorkeys DynamoDB Load Tool"
    )
    parser.add_argument(
        "-f", "--files",
        action = "append",
        help = "File(s) to process",
        nargs = "+",
        required = True,
        type = str,
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
        "-v", "--version",
        action = "version",
        version = pkg_resources.get_distribution(parser.prog).version,
        help = "Show version number and exit",
    )
    args = vars(parser.parse_args(args))
    return args


def run(args):
    project_name = (os.path.dirname(__file__).split("/")[-1])
    my_cli = clihelper.CLI(project_name, args)
    # logger = my_cli.logger
    logger_noformat = my_cli.logger_noformat
    my_cli.print_versions()

    # Get CLI args.
    filepaths = args["files"]
    jsonfiles = filepath.get_files(filepaths, CONSTANTS().JSON_SUFFIXES)
    for filename in jsonfiles:
        colorkeys = get_colorkeys_from_json(filename)
        logger_noformat.info(colorkeys)
        # response = load_dynamodb(site, table, colorkeys)
        # logger.debug(response)
    return None


def get_colorkeys_from_json(filename):
    with open(filename) as f:
        str_ = f.read()
    colorkeys = json.loads(str_)
    return colorkeys


def load_dynamodb(site, table, colorkeys):
    if site == "cloud":
        db = boto3.resource("dynamodb")
    elif site == "local":
        db = boto3.resource(
            "dynamodb",
            endpoint_url=CONSTANTS().DYNAMODB_URL_LOCAL
        )
    tbl = db.Table(table)
    for colorkey in colorkeys:
        h = colorkey["histogram"]
        selector = (
            f'{h["algo"]}#{h["colorspace"]}#{h["n_clusters"]}#'
            f'{colorkey["cpu"]}#{colorkey["memory"]}#{colorkey["timestamp"]}'
        )
        # logger.info(f"selector: {selector}")
        colorkey["selector"] = selector
        response = tbl.put_item(Item=colorkey)
    return response


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

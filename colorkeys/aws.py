#!/usr/bin/env python3

"""
This module facilitates accessing AWS resources for CI/CD. It requires AWS
credentials preexisting in the environment.

    Typical Usage:

    my_aws = AWS()
"""

import boto3
import botocore.exceptions
import io
import logging
import zipfile

from boto3.dynamodb.conditions import Key
from colorkeys.constants import _const as CONSTANTS

logger = logging.getLogger(__name__)


class AWS():
    """A class for accessing the ECS task running colorkeys and storing the
    generated data.

    Attributes:
        task_arn (str): ARN of task running colorkeys.
        task_hash (str): hash of task running colorkeys.
        task_desc (dict): Task description as defined in ECS.
    """
    def __init__(self):
        """Init AWS.

        Args:
            None
        """
        self.ecs = boto3.client("ecs")
        self.s3 = boto3.client("s3")
        self._task_arn = self._get_task_arn()
        self._task_hash = self._get_task_hash()
        self._task_desc = self._get_task_desc()

    @property
    def task_arn(self):
        """Task ARN."""
        return self._task_arn

    @property
    def task_hash(self):
        """Task hash."""
        return self._task_hash

    @property
    def task_desc(self):
        """Task description."""
        return self._task_desc

    def upload_S3(self, bucket, obj):
        """Upload JSON-encoded object to S3."""
        return self._upload_S3(bucket, obj)

    def _upload_S3(self, bucket, obj):
        """Upload JSON-encoded object to S3 bucket.

        Args:
            bucket (str): Bucket name.
            obj (str): JSON-encoded object.

        Returns:
            None

        """
        jsonfile = f"{self._task_hash[:8]}.colorkeys.json"
        my_bucket = bucket
        my_key = f"{jsonfile}.zip"
        logger.debug(f"my_key: {my_key}")
        logger.debug(f"my_bucket: {my_bucket}")
        zbuffer = io.BytesIO()
        zf = zipfile.ZipFile(zbuffer, "w")
        zf.writestr(jsonfile, obj)
        zf.close()
        zbuffer.seek(0)
        self.s3.upload_fileobj(zbuffer, my_bucket, my_key)
        return None

    def _get_task_arn(self):
        """Get the ARN of task running colorkeys."""
        dict_ = self.ecs.list_tasks(
            cluster = "workers",
            family = "stage-colorkeys-run",
            maxResults = 1,
        )
        task_arn = next(i for i in dict_["taskArns"])
        logger.debug(f"task_arn: {task_arn}")
        return task_arn

    def _get_task_hash(self):
        """Get the hash (end of ARN) of task running colorkeys."""
        task_hash = self._task_arn.split("/")[-1]
        logger.debug(f"task_hash: {task_hash}")
        return task_hash

    def _get_task_desc(self):
        """Get the task description by task ARN."""
        dict_ = self.ecs.describe_tasks(
            cluster = "workers",
            tasks = [self._task_arn],
        )
        task_desc = next(i for i in dict_["tasks"])
        return task_desc


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
        logger.debug(f"selector: {selector}")
        colorkey["selector"] = selector
        try:
            response = tbl.put_item(
                Item=colorkey,
                ConditionExpression=(
                    Key("filehash").not_exists() & Key("selector").not_exists()
                )
            )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise
    return response


def query_dynamodb(site, table, filehash, algo, colorspace, n_clusters, **kwargs):
    if site == "cloud":
        db = boto3.resource("dynamodb")
    elif site == "local":
        db = boto3.resource(
            "dynamodb",
            endpoint_url=CONSTANTS().DYNAMODB_URL_LOCAL
        )
    tbl = db.Table(table)
    selector = f'{algo}#{colorspace}#{n_clusters}'
    response = tbl.query(
        KeyConditionExpression=(
            Key("filehash").eq(filehash) & Key("selector").begins_with(selector)
        )
    )
    return response

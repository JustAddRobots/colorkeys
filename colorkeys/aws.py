#!/usr/bin/env python3

"""
This module facilitates accessing AWS resources for CI/CD. It requires AWS
credentials preexisting in the environment.

    Typical Usage:

    my_aws = AWS()
"""

import boto3
import io
import logging
import json
import zipfile

logger = logging.getLogger(__name__)


class AWS():
    """A class for accessing the ECS task running colorkeys and storing the
    generated data.

    Attributes:
        task_arn (str): ARN of task running colorkeys.
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
    def task_desc(self):
        """Task description."""
        return self._task_desc

    def upload_S3(self, obj):
        """Upload JSON-encoded object to S3."""
        return self._upload_S3(obj)

    def _upload_S3(self, obj):
        """Upload JSON-encoded object to temporary S3 bucket.

        Args:
            obj (str): JSON-encoded object.

        Returns:
            None

        """
        jsonfile = f"{self._task_hash[:8]}.colorkeys.json"
        my_bucket = "colorkeys-tmp"
        my_key = f"{jsonfile}.zip"
        logger.debug(f"my_key: {my_key}")
        logger.debug(f"my_bucket: {my_bucket}")
        zbuffer = io.BytesIO()
        zf = zipfile.ZipFile(zbuffer, "w")
        zf.writestr(jsonfile, json.dumps(obj))
        zf.close()
        zbuffer.seek(0)
        self.s3.upload_fileobj(zbuffer, my_bucket, my_key)
        return None

    def _get_task_arn(self):
        """Get the ARN of task running colorkeys."""
        dict_ = self.ecs.list_tasks(
            cluster = "workers",
            family = "colorkeys-deploy",
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

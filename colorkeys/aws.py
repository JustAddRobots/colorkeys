#!/usr/bin/env python3

import boto3
import io
import logging
import json
import zipfile

logger = logging.getLogger(__name__)


class AWS():

    def __init__(self):
        self.ecs = boto3.client("ecs")
        self.s3 = boto3.client("s3")
        self._task_arn = self._get_task_arn()
        self._task_hash = self._get_task_hash()
        self._task_desc = self._get_task_desc()

    @property
    def task_arn(self):
        return self._task_arn

    @property
    def task_desc(self):
        return self._task_desc

    def upload_S3(self, obj):
        return self._upload_S3(obj)

    def _upload_S3(self, obj):
        jsonfile = f"{self._task_hash[:8]}.colorkeys.json"
        my_bucket = "colorkeys-tmp"
        my_key = f"{jsonfile}.zip"
        logger.debug(f"my_key: {my_key}")
        logger.debug(f"my_bucker: {my_bucket}")
        stream = io.BytesIO()
        zf = zipfile.ZipFile(stream, "w")
        zf.writestr(jsonfile, json.dumps(obj))
        zf.close()
        self.s3.upload_fileobj(zf, my_bucket, my_key)
        return

    def _get_task_arn(self):
        dict_ = self.ecs.list_tasks(
            cluster = "workers",
            family = "colorkeys-deploy",
            maxResults = 1,
        )
        task_arn = next(i for i in dict_["taskArns"])
        logger.debug(f"task_arn: {task_arn}")
        return task_arn

    def _get_task_hash(self):
        task_hash = self._task_arn.split("/")[-1]
        logger.debug(f"task_hash: {task_hash}")
        return task_hash

    def _get_task_desc(self):
        dict_ = self.ecs.describe_tasks(
            cluster = "workers",
            tasks = [self._task_arn],
        )
        task_desc = next(i for i in dict_["tasks"])
        return task_desc

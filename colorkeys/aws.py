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
        self._container_arn = self._get_container_arn()

    @property
    def task_arn(self):
        return self._task_arn

    @property
    def task_desc(self):
        return self._task_desc

    @property
    def container_arn(self):
        return self._container_arn

    @property
    def container_runtime_id(self):
        return self._container_runtime_id

    @property
    def upload_S3(self, obj):
        return self._upload_S3(obj)

    def _upload_S3(self, obj):
        jsonfile = f"{self._task_hash}.colorkeys.json"
        my_bucket = "colorkeys-tmp"
        my_key = f"{jsonfile}.zip"
        stream = io.BytesIO()
        zf = zipfile.Zipfile(stream, "wb")
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
        task_desc = self.ecs.describe_tasks(tasks=self._task_arn)
        return task_desc

    def _get_container_arn(self):
        dict_ = self.ecs.list_container_instances(
            cluster = "workers",
            filter = "task:group == family:colorkeys-deploy",
            maxResults = 1,
        )
        container_arn = next(i for i in dict_["containerInstanceArns"])
        logger.debug(f"container_arn: {container_arn}")
        return container_arn

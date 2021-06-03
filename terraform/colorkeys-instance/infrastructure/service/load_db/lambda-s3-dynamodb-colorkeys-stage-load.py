import boto3
import io
import logging
import json
import zipfile
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_input_artifact(job, key):
    logger.info(f"key: {key}")
    s3_input = next(i for i in job["data"]["inputArtifacts"])["location"]["s3Location"]
    bucket = s3_input["bucketName"]
    objkey = s3_input["objectKey"]
    obj = get_obj_from_s3zip(bucket, objkey, "imagedefinitions.json")
    artifact = next(i[key] for i in obj if i["name"] == "colorkeys")
    logger.info(f"artifact: {artifact}")
    return artifact


def get_user_param(job, key):
    task_arn = job["data"]["actionConfiguration"]["configuration"]["UserParameters"]
    logger.info(f"task_arn: {task_arn}")
    return task_arn


def get_obj_from_s3zip(bucket, objkey, internalfile):
    s3 = boto3.resource("s3")
    logger.info(f"bucket: {bucket}")
    logger.info(f"objkey: {objkey}")
    s3obj = s3.Object(bucket, objkey)
    with zipfile.ZipFile(io.BytesIO(s3obj.get()["Body"].read())) as zf:
        with zf.open(internalfile) as obj_json:
            obj = json.loads(obj_json.read().decode(), parse_float=Decimal, parse_int=int)
    return obj


def get_task_obj(task_hash):
    bucket = "colorkeys-tmp"
    internalfile = f"{task_hash[:8]}.colorkeys.json"
    objkey = f"{internalfile}.zip"
    obj = get_obj_from_s3zip(bucket, objkey, internalfile)
    logger.info(f"obj: {obj}")
    return obj


def load_colorkeys(colorkeys):
    db = boto3.resource("dynamodb")
    tbl = db.Table("colorkeys-stage")
    for colorkey in colorkeys:
        h = colorkey["histogram"]
        selector = (
            f'{h["algo"]}#{h["colorspace"]}#{h["n_clusters"]}#'
            f'{colorkey["cpu"]}#{colorkey["memory"]}#{colorkey["timestamp"]}'
        )
        logger.info(f"selector: {selector}")
        colorkey["selector"] = selector
        response = tbl.put_item(Item=colorkey)
    return response


def lambda_handler(event, context):
    job = event["CodePipeline.job"]
    logging.info(job)
    cp = boto3.client("codepipeline")
    try:
        task_arn = get_user_param(job, "task_arn")
        task_hash = task_arn.split("/")[-1]
        colorkeys = get_task_obj(task_hash)
        r = load_colorkeys(colorkeys)
    except Exception as e:
        logger.info("Lambda Failure")
        logger.info(str(e))
        cp.put_job_failure_result(
            jobId = job["id"],
            failureDetails = {"message": str(e), "type": "JobFailed"}
        )
    else:
        logger.info(r)
        cp.put_job_success_result(
            jobId = job["id"],
        )
    logger.info("Lambda Complete")
    return None

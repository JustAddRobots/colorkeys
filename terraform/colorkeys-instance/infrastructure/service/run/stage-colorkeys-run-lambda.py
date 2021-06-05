import boto3
import io
import logging
import json
import zipfile

logger = logging.getLogger()
logger.setLevel(logging.INFO)


FARGATE_CLUSTER = "workers"
FARGATE_TASK_DEF = "colorkeys-deploy:13"
FARGATE_SUBNET_ID = "subnet-2c7ff84a"
FARGATE_SECURITY_GROUP_ID = "sg-0754b7137e6715e16"
ARTIFACT_FILE = "imagedefinitions.json"


def run_fargate_task(img):
    ecs = boto3.client("ecs")
    response = ecs.run_task(
        cluster = FARGATE_CLUSTER,
        count = 1,
        launchType = "FARGATE",
        networkConfiguration = {
            "awsvpcConfiguration": {
                "subnets": [
                    FARGATE_SUBNET_ID,
                ],
                "securityGroups": [
                    FARGATE_SECURITY_GROUP_ID,
                ],
                "assignPublicIp": "ENABLED"
            }
        },
        taskDefinition = FARGATE_TASK_DEF
    )
    return response


def get_input_artifact(job, key):
    logger.info(f"key: {key}")
    s3_input = next(i for i in job["data"]["inputArtifacts"])["location"]["s3Location"]
    bucket = s3_input["bucketName"]
    objkey = s3_input["objectKey"]
    s3 = boto3.resource("s3")
    logger.info(f"bucket: {bucket}")
    logger.info(f"objkey: {objkey}")
    s3obj = s3.Object(bucket, objkey)
    with zipfile.ZipFile(io.BytesIO(s3obj.get()["Body"].read())) as zf:
        with zf.open(ARTIFACT_FILE) as imgdef:
            obj = json.loads(imgdef.read().decode())
    artifact = next(i[key] for i in obj if i["name"] == "colorkeys")
    logger.info(f"artifact: {artifact}")
    return artifact


def lambda_handler(event, context):
    job = event["CodePipeline.job"]
    cp = boto3.client("codepipeline")
    try:
        logger.info(f"job: {job}")
        img = get_input_artifact(job, "imageUri")
        r = run_fargate_task(img)
        task_arn = r["tasks"][0]["taskArn"]
        ecs = boto3.client("ecs")
        waiter = ecs.get_waiter("tasks_stopped")
        logger.info(f"Waiting for {task_arn}")
        waiter.wait(cluster="workers", tasks=[task_arn])
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
            outputVariables = {
                "task_arn": task_arn
            }
        )
    logger.info("Lambda Complete")
    return None

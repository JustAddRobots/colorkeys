import boto3
import io
import logging
import json
import re
import zipfile

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_cluster_name(env):
    ecs = boto3.client("ecs")
    cluster = ""
    for c in ecs.list_clusters()["clusterArns"]:
        for t in ecs.list_tags_for_resource(c)["tags"]:
            if t["key"] == "environment" and t["value"] == env:
                regex = ".*cluster/([a-zA-Z0-9]+)"
                m = re.search(regex, c)
                if m:
                    cluster = m.groups()[0]
    return cluster


def get_subnet_id(env):
    ec2 = boto3.client("ec2")
    filters = [{"Name": "tag:environment", "Values": [env]}]
    subnet = next(i for i in list(ec2.subnets.filter(Filters=filters)))
    return subnet.id


def get_security_group_id(env):
    ec2 = boto3.client("ec2")
    filters = [{"Name": "tag:environment", "Values": [env]}]
    sg = next(i for i in list(ec2.security_groups.filter(Filters=filters)))
    return sg.id


def get_task_definition(env):
    ecs = boto3.client("ecs")
    dict_ = ecs.list_task_definitions(
        familyPrefix = f"{env}-colorkeys-run",
        status = "ACTIVE",
        sort = "DESC",
        maxResults = 1
    )
    task_arn = next(i for i in dict_["taskDefinitionArns"])
    return task_arn


def run_fargate_task(img):
    env = "stage"
    ecs = boto3.client("ecs")
    response = ecs.run_task(
        cluster = get_cluster_name(env),
        count = 1,
        launchType = "FARGATE",
        networkConfiguration = {
            "awsvpcConfiguration": {
                "subnets": [
                    get_subnet_id(env),
                ],
                "securityGroups": [
                    get_security_group_id(env),
                ],
                "assignPublicIp": "ENABLED"
            }
        },
        taskDefinition = get_task_definition(env)
    )
    return response


def get_input_artifact(job, artifact_file, key):
    logger.info(f"key: {key}")
    s3_input = next(i for i in job["data"]["inputArtifacts"])["location"]["s3Location"]
    bucket = s3_input["bucketName"]
    objkey = s3_input["objectKey"]
    s3 = boto3.resource("s3")
    logger.info(f"bucket: {bucket}")
    logger.info(f"objkey: {objkey}")
    s3obj = s3.Object(bucket, objkey)
    with zipfile.ZipFile(io.BytesIO(s3obj.get()["Body"].read())) as zf:
        with zf.open(artifact_file) as imgdef:
            obj = json.loads(imgdef.read().decode())
    artifact = next(i[key] for i in obj if i["name"] == "colorkeys")
    logger.info(f"artifact: {artifact}")
    return artifact


def lambda_handler(event, context):
    job = event["CodePipeline.job"]
    cp = boto3.client("codepipeline")
    try:
        logger.info(f"job: {job}")
        img = get_input_artifact(job, "imagedefinitions.json", "imageUri")
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

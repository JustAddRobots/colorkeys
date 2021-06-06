# === run ===

### ECS ###

data "aws_iam_policy" "ecs_task_exec" {
  arn   = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  tags  = var.default_tags
}

resource "aws_iam_policy" "ecs_task_exec_boto3" {
  description = "ECS Task Policy"
  name        = "stage-ecs-task-exec_boto3"
  tags        = var.default_tags
  policy      = data.aws_iam_policy_document.ecs_task_exec_boto3.json
}

resource "aws_iam_role" "ecs_task_exec" {
  name                = "stage-ecs-task_exec"
  tags                = var.default_tags
  assume_role_policy  = jsonencode({
    Version    = "2012-10-17"
    Statement  = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_exec" {
  role        = "${aws_iam_role.ecs_task_exec.name}"
  policy_arn  = "${data.aws_iam_policy.ecs_task_exec.arn}"
}

resource "aws_iam_role_policy_attachment" "ecs_task_exec_boto3" {
  role        = "${aws_iam_role.ecs_task_exec.name}"
  policy_arn  = "${aws_iam_policy.ecs_task_exec_boto3.arn}"
}

data "aws_iam_policy" "ecs_service" {
  arn   = "arn:aws:iam::aws:policy/aws-service-role/AmazonECSServiceRolePolicy"
  tags  = var.default_tags
}

resource "aws_iam_role" "ecs_service" {
  name                = "stage-ecs-service"
  tags                = var.default_tags
  assume_role_policy  = jsonencode({
    Version     = "2012-10-17"
    Statement   = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "ecs.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_service" {
  role        = "${aws_iam_role.ecs_service.name }"
  policy_arn  = "${data.aws_iam_policy.ecs_service.arn}"
}

resource "aws_ecs_task_definition" "stage_colorkeys-run" {
  family                    = "stage-colorkeys-run"
  execution_role_arn        = "${aws_iam_role.ecs_service.arn}"
  task_role_arn             = "${aws_iam_role.ecs_task_exec.arn}"
  network_mode              = "awsvpc"
  requires_compatibilities  = ["FARGATE"]
  cpu                       = "512"
  memory                    = "1024"
  tags                      = var.default_tags

  container_definitions = <<CONTAINER_DEFINITION
[
    {
        "name": "${var.env}-colorkeys-run",
        "image": "${var.image}"
        "cpu": 512,
        "portMappings": [
            {
                "containerPort": 443,
                "hostPort": 443,
                "protocol": "tcp"
            }
        ],
        "essential": true,
        "environment": [
            {
                "name": "IMAGES",
                "value": "${var.samples}"
            },
            {
                "name": "N_CLUSTERS",
                "value": "-n 7"
            },
            {
                "name": "COLORSPACES",
                "value": "-c HSV RGB"
            },
            {
                "name": "AWS",
                "value": "--aws"
            },
            {
                "name": "DEBUG",
                "value": "--debug"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "/ecs/${var.env}-colorkeys-run",
                "awslogs-region": "us-west-1",
                "awslogs-stream-prefix": "ecs"
            }
        }
    }
]
CONTAINER_DEFINITION

}

resource "aws_ecs_cluster" "workers" {
  name  = "workers"
  capacity_providers  = [
    "FARGATE",
    "FARGATE_SPOT"
  ]
  setting {
    name  = "containerInsights"
    value = "disabled"
  }
  tags  = var.default_tags
}
  
### Lambda ###

resource "aws_iam_policy" "lambda_run" {
  description = "Lambda ECS Policy"
  name        = "stage-lambda-run"
  tags        = var.default_tags
  policy      = data.aws_iam_policy_document.lambda_run.json
}

resource "aws_iam_role" "lambda_run" {
  name  = "stage-lambda-run"
  tags  = var.default_tags
  assume_role_policy  = jsonencode({
    Version     = "2012-10-17"
    Statement  = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_run" {
  role        = "${aws_iam_role.lambda_run.name}"
  policy_arn  = "${aws_iam_policy.lambda_run.arn}"
}
  
data "archive_file" "stage_lambda_run" {
  type        = "zip"
  source_file = "${path.module}/${var.stage_lambda_run_source}"
  output_path = "${path.module}/${var.stage_lambda_run_zip}"
}

resource "aws_lambda_function" "run" {
  description   = "Run colorkeys against standardised images"
  filename      = "${var.stage_lambda_run_zip}"
  function_name = "${var.stage_lambda_run_funcname}"
  role          = "${aws_iam_role.lambda_run.arn}"
  handler       = "${var.stage_lambda_run_funcname}.lambda_handler"
  tags          = var.default_tags
  
  runtime = "python3.8"
  timeout = "300"
  vpc_config {
    subnet_ids          = [
      "${aws_subnet.stage_colorkeys_public_0.id}",
      "${aws_subnet.stage_colorkeys_public_1.id}"
    ]
    security_group_ids  = [
      "${aws_security_group.stage_colorkeys_https.id}"
    ]
  }
}

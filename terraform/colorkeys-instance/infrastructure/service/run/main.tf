# === run ===

### ECS task ###

resource "aws_iam_policy" "ecs_task_exec" {
  description = "ECS Task Policy"
  name        = "stage-ecs-task-exec"
  tags        = var.default_tags
  policy      = data.aws_iam_policy_document.ecs_task_exec.json
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
  policy_arn  = "${aws_iam_policy.ecs_task_exec.arn}"
}

resource "aws_iam_policy" "ecs_service" {
  description = "ECS Service Policy"
  name        = "stage-ecs-service"
  tags        = var.default_tags
  policy      = data.aws_iam_policy_document.ecs_service.json
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
  role        = "${aws_iam_policy.ecs_service.name }"
  policy_arn  = "${aws_iam_policy.ecs_service.arn}"
}

### Lambda ###

resource "aws_iam_policy" "lambda_ecs" {
  description = "Lambda ECS Policy"
  name        = "stage-lambda-ecs"
  tags        = var.default_tags
  policy      = data.aws_iam_policy_document.lambda_ecs.json
}

resource "aws_iam_role" "lambda_ecs" {
  name  = "stage-lambda-ecs"
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

resource "aws_iam_role_policy_attachment" "lambda_ecs" {
  role        = "${aws_iam_role.lambda_ecs.name}"
  policy_arn  = "${aws_iam_policy.lambda_ecs.arn}"
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
  tags  = vars.default_tags
}

resource "aws_ecs_task_definition" "stage_colorkeys-run" {
  family                    = "stage-colorkeys-run"
  execution_role_arn        = ""
  task_role_arn             = ""
  cpu                       = "512"
  memory                    = "1024"
  network_mode              = "awsvpc"
  requires_compatibilities  = "FARGATE"
  tags                      = var.default_tags

  container_definitions = <<CONTAINER_DEFINITION
[
    {
        "name": "${var.run_container_name}",
        "image": ""
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
                "value": ""
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
                "awslogs-group": "/ecs/colorkeys-deploy",
                "awslogs-region": "us-west-1",
                "awslogs-stream-prefix": "ecs"
            }
        }
    }
]
CONTAINER_DEFINITION

}

resource "aws_lambda_function" "run_ecs" {
  description   = "Run colorkeys against standardised images"
  filename      = "stage-colorkeys-run-lambda.zip"
  function_name = "stage-colorkeys-run-lambda"
  role          = "${aws_iam_role.lambda_ecs.arn}"
  handler       = "stage-colorkeys-run.lambda_handler"
  tags          = var.default_tags
  
  runtime = "python3.8"
  timeout = "300"
  
  

# pipeline

data "aws_caller_identity" "current" {}

locals {
  aws_account_id                      = data.aws_caller_identity.current.account_id
  codepipeline_source_connection_arn  = "arn:aws:codestar-connections:${var.aws_region}:${local.aws_account_id}:connection/fdf2d69f-c7cc-4d2c-93f4-0915b85d9c30"
}

resource "aws_s3_bucket" "this" {
  bucket        = "${var.codepipeline_artifact_bucket}"
  acl           = "private"
  tags          = var.default_tags
  force_destroy = true
}

resource "aws_ecr_repository" "stage_colorkeys_build_repo" {
  name  = "${var.codepipeline_build_repo}"
  tags  = var.default_tags
}

resource "aws_iam_policy" "codepipeline_service" {
  name        = "codepipeline-service"
  description = "CodePipeline Service Policy"
  tags        = var.default_tags
  policy      = data.aws_iam_policy_document.codepipeline_service.json
}

resource "aws_iam_role" "codepipeline_service" {
  name                = "codepipeline-service"
  tags                = var.default_tags
  assume_role_policy  = jsonencode({
    Version     = "2012-10-17"
    Statement  = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "codepipeline.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "codepipeline_service" {
  role        = "${aws_iam_role.codepipeline_service.name}"
  policy_arn  = "${aws_iam_policy.codepipeline_service.arn}"
}

module "build" {
  source            = "../build"
  build_projectname = "${var.codepipeline_build_projectname}"
  build_ecr_repo    = "${aws_ecr_repository.stage_colorkeys_build_repo.repository_url}"
}

# # === codepipeline_build ===
# 
# resource "aws_iam_policy" "codebuild_service" {
#   name        = "codebuild-service"
#   description = "CodeBuild Service Role"
#   tags        = var.default_tags
#   policy      = data.aws_iam_policy_document.codebuild_service.json
# }
# 
# resource "aws_iam_policy" "ecr_push" {
#   name        = "ecr-push"
#   description = "Push to ECR"
#   tags        = var.default_tags
#   policy      = data.aws_iam_policy_document.ecr_push.json
# }
# 
# resource "aws_iam_policy" "codestar_github" {
#   name        = "codestar-github"
#   description = "Connect to github"
#   tags        = var.default_tags
#   policy      = data.aws_iam_policy_document.codestar_github.json
# }
# 
# resource "aws_iam_role" "codebuild_service" {
#   name                = "codebuild-service"
#   assume_role_policy  = jsonencode({
#     Version   = "2012-10-17",
#     Statement = [
#       {
#         Action    = "sts:AssumeRole",
#         Effect    = "Allow",
#         Principal = {
#           Service = "codebuild.amazonaws.com"
#         }
#       }
#     ]
#   })
# }
# 
# resource "aws_iam_role_policy_attachment" "codebuild_service" {
#   role        = "${aws_iam_role.codebuild_service.name}"
#   policy_arn  = "${aws_iam_policy.codebuild_service.arn}"
# }
# 
# resource "aws_iam_role_policy_attachment" "ecr_push" {
#   role        = "${aws_iam_role.codebuild_service.name}"
#   policy_arn  = "${aws_iam_policy.ecr_push.arn}"
# }
# 
# resource "aws_iam_role_policy_attachment" "codestar_github" {
#   role        = "${aws_iam_role.codebuild_service.name}"
#   policy_arn  = "${aws_iam_policy.codestar_github.arn}"
# }
# 
# resource "aws_codebuild_project" "stage-colorkeys-build" {
#   name          = "${var.codepipeline_build_projectname}"
#   description   = "Colorkeys Docker build"
#   build_timeout = "5"
#   service_role  = "${aws_iam_role.codebuild_service.arn}"
#   tags          = var.default_tags
# 
#   artifacts {
#     type                = "CODEPIPELINE"
#     name                = "build_artifact"
#     packaging           = "NONE"
#     encryption_disabled = false
#   }
# 
#   cache {
#     type  = "NO_CACHE"
#   }
# 
#   environment {
#     compute_type                = "BUILD_GENERAL1_SMALL"
#     image                       = "aws/codebuild/amazonlinux2-x86_64-standard:3.0"
#     type                        = "LINUX_CONTAINER"
#     image_pull_credentials_type = "CODEBUILD"
#     privileged_mode             = true
# 
#     environment_variable {
#       name  = "AWS_ACCOUNT_ID"
#       value = local.aws_account_id
#       type  = "PLAINTEXT"
#     }
# 
#     environment_variable {
#       name  = "AWS_DEFAULT_REGION"
#       value = "${var.aws_region}"
#       type  = "PLAINTEXT"
#     }
# 
#     environment_variable {
#       name  = "ECR_REPO"
#       value = "${aws_ecr_repository.stage_colorkeys_build_repo.repository_url}"
#       type  = "PLAINTEXT"
#     }
# 
#     environment_variable {
#       name  = "ENGCOMMON_BRANCH"
#       value = "main"
#       type  = "PLAINTEXT"
#     }
# 
#   }
# 
#   logs_config {
#     cloudwatch_logs {
#       status  = "ENABLED"
#     }
#     s3_logs {
#       status              = "DISABLED"
#       encryption_disabled = false
#     }
#   }
# 
#   source {
#     type            = "CODEPIPELINE"
#     git_clone_depth = 0
#     insecure_ssl    = false
#   }
# 
#   concurrent_build_limit  = 1
# }  

# === codepipeline ===
resource "aws_codepipeline" "codepipeline" {
  name      = "stage-colorkeys"
  role_arn  = "${aws_iam_role.codepipeline_service.arn}"
  tags      = var.default_tags

  artifact_store {
    location  = "${var.codepipeline_artifact_bucket}"
    type      = "S3"
  }

    

  stage {
    name = "Source"

    action {
      name              = "source-colorkeys"
      category          = "Source"
      owner             = "AWS"
      provider          = "CodeStarSourceConnection"
      version           = "1"
      output_artifacts  = ["source_artifact"]
      namespace         = "codepipeline-source"

      configuration = {
        ConnectionArn         = "${local.codepipeline_source_connection_arn}"
        FullRepositoryId      = "${var.codepipeline_source_repo}"
        BranchName            = "${var.codepipeline_source_branch}"
        DetectChanges         = "true"
        OutputArtifactFormat  = "CODEBUILD_CLONE_REF"
      }
    }
  }

  stage {
    name = "Build"

    action {
      name              = "build-colorkeys"
      category          = "Build"
      owner             = "AWS"
      provider          = "CodeBuild"
      version           = "1"
      input_artifacts   = ["source_artifact"]
      output_artifacts  = ["build_artifact"]
      namespace         = "codepipeline-build"

      configuration     = {
        ProjectName     = "${var.codepipeline_build_projectname}"
      }
    }
  }

#   stage {
#     name = "Run"
# 
#     action {
#       name              = "run-colorkeys"
#       category          = "Invoke"
#       owner             = "AWS"
#       provider          = "Lambda"
#       input_artifacts   = ["build_artifact"]
#       output_artifacts  = ["run_output"]
#       version           = "1"
#       namespace         = "codepipeline-run"
# 
#       configuration     = {
#         FunctionName    = "${var.codepipeline_run_funcname}"
#       }
#     }
#   }
# 
#   stage {
#     name = "Load"
# 
#     action {
#       name              = "load-colorkeys"
#       category          = "Invoke"
#       owner             = "AWS"
#       provider          = "Lambda"
#       input_artifacts   = []
#       output_artifacts  = ["load_output"]
#       version           = "1"
#       namespace         = "codepipeline-load"
# 
#       configuration = {
#         FunctionName    = "${var.codepipeline_load_funcname}"
#         UserParamaters  = "#${codepipeline_run.task_arn}"
#       }
#     }
#   }

}

# === codepipeline_run === 
# resource "aws_iam_policy" "this" {
#   name  = "stage-codepipeline-colorkeys-policy"
#   path  = "/"
# 
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Effect  = "Allow",
#         Action  = [
#           "codepipeline:PutJobFailureResult",
#           "codepipeline:PutJobSuccessResult"
#         ],
#         Resource  = "*"
#       },
#       {
#         Effect = "Allow",
#         Action = [
#           "s3:PutObject",
#           "s3:GetObject",
#           "s3:ListBucket",
#         ],
#         Resource = [
#           "arn:aws:s3:::${var.codepipeline_artifact_bucket}",
#         ]
#       },
#       {
#         Effect = "Allow",
#         Action = "logs:*",
#         Resource = "arn:aws:logs:*:*:*"
#       }
#     ]
#   })
# }

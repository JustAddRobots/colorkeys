variable "codepipeline_artifact_bucket" {
  default = "stage-codepipeline-artifact"
}

variable "codepipeline_source_repo" {
  default = "JustAddRobots/colorkeys"
}

variable "codepipeline_source_branch" {
  default = "stage"
}

variable "codepipeline_build_projectname" {
  default = "stage-colorkeys-build"
}

variable "codepipeline_build_repo" {
  default = "stage-colorkeys"
}

variable "codepipeline_run_funcname" {
  default = "stage-colorkeys-run-lambda"
}

variable "codepipeline_run_bucket" {
  default = "stage-colorkeys-run"
}

variable "codepipeline_load_funcname" {
  default = "stage-colorkeys-load-lambda"
}

variable "codepipeline_load_bucket" {
  default = "stage-colorkeys-load"
}

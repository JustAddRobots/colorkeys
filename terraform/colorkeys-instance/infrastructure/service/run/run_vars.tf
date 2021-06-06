variable "image" {
  description = "ECR repo build image"
  type        = string
}

variable "samples" {
  description = "S3 URI for image samples"
  type        = string
}

variable "stage_lambda_run_source" {
  description = "Lambda source"
  type        = string
  default     = "./stage-colorkeys-run-lambda.py"
}

variable "stage_lambda_run_zip" {
  description = "Lambda zip"
  type        = string
  default     = "./stage-colorkeys-run-lambda.py.zip"
}

variable "stage_lambda_run_funcname" {
  description = "Lambda functioin name"
  type        = string
  default     = "stage-colorkeys-run-lambda"
}

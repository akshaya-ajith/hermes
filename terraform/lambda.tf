provider "aws" {
  region = "us-east-2"
  profile = "AdministratorAccess-344988460867"
}
# the IAM Role for Lambda Execution
resource "aws_iam_role" "lambda_exec" {
  name = "translate_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# attaching basic logging permissions
resource "aws_iam_role_policy_attachment" "lambda_logging" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# attaching the Amazon Translate permissions
# resource "aws_iam_role_policy_attachment" "translate_permissions" {
#   role       = aws_iam_role.lambda_exec.Transl
#   policy_arn = "arn:aws:iam::aws:policy/AmazonTranslateFullAccess"
# }

# not sure
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/dispatch.py"
  output_path = "${path.module}/lambda.zip"
}

# defining lambda
resource "aws_lambda_function" "hermes_dispatch" {
  function_name = "HermesDispatch"

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  handler = "dispatch.lambda_handler"
  runtime = "python3.11"
  timeout = 10

  role = aws_iam_role.lambda_exec.arn
}

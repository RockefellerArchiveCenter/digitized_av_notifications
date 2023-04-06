data "archive_file" "lambda" {
  type        = "zip"
  source_file = "handle_digitized_av_notifications.py"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "handle_digitized_av_notifications" {
  filename      = "${data.archive_file.lambda.output_path}"
  function_name = "digitized_av_notifications"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "handle_digitized_av_notifications.lambda_handler"

  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.9"

  environment {
    variables = {
      "TEAMS_URL" = var.teams_url
    }
  }
}

resource "null_resource" "sam_metadata_aws_lambda_function_handle_digitized_av_notifications" {
  triggers = {
    resource_name = "aws_lambda_function.handle_digitized_av_notifications"
    resource_type = "ZIP_LAMBDA_FUNCTION"
    original_source_code = "${data.archive_file.lambda.source_file}"
    built_output_path = "${data.archive_file.lambda.output_path}"
  }
}
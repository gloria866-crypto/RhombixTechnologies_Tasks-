# Step 9: CloudWatch and SNS monitoring for the photo gallery.

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/cloud-photo-gallery"
  retention_in_days = 14

  tags = {
    Application = "cloud-photo-gallery"
    Purpose     = "lambda-logs"
  }
}

resource "aws_sns_topic" "photo_gallery_alerts" {
  name = "cloud-photo-gallery-alerts"

  tags = {
    Application = "cloud-photo-gallery"
    Purpose     = "notifications"
  }
}

resource "aws_sns_topic_subscription" "photo_gallery_alert_email" {
  topic_arn = aws_sns_topic.photo_gallery_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

resource "aws_cloudwatch_metric_alarm" "lambda_error_rate" {
  alarm_name          = "cloud-photo-gallery-lambda-errors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Alarm when any Lambda function errors occur."
  treat_missing_data  = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.generate_upload_url.function_name
  }

  alarm_actions = [aws_sns_topic.photo_gallery_alerts.arn]
}

resource "aws_cloudwatch_metric_alarm" "api_5xx_errors" {
  alarm_name          = "cloud-photo-gallery-api-5xx"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "5XXErrors"
  namespace           = "AWS/ApiGateway"
  period              = "300"
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Alarm when API Gateway returns 5xx responses."
  treat_missing_data  = "notBreaching"

  dimensions = {
    ApiName = aws_apigatewayv2_api.photo_gallery.name
  }

  alarm_actions = [aws_sns_topic.photo_gallery_alerts.arn]
}

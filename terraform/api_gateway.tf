# Step 6: HTTP API routes for the gallery Lambda functions.
resource "aws_apigatewayv2_api" "photo_gallery" {
  name          = "cloud-photo-gallery-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["http://localhost:3000"]
    allow_methods = ["GET", "POST", "DELETE", "OPTIONS"]
    allow_headers = ["Content-Type"]
    max_age       = 3600
  }
}

resource "aws_apigatewayv2_integration" "generate_upload_url" {
  api_id                 = aws_apigatewayv2_api.photo_gallery.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.generate_upload_url.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "get_photos" {
  api_id                 = aws_apigatewayv2_api.photo_gallery.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.get_photos.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "delete_photo" {
  api_id                 = aws_apigatewayv2_api.photo_gallery.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.delete_photo.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "upload_url" {
  api_id    = aws_apigatewayv2_api.photo_gallery.id
  route_key = "POST /upload-url"
  target    = "integrations/${aws_apigatewayv2_integration.generate_upload_url.id}"
}

resource "aws_apigatewayv2_route" "photos" {
  api_id    = aws_apigatewayv2_api.photo_gallery.id
  route_key = "GET /photos"
  target    = "integrations/${aws_apigatewayv2_integration.get_photos.id}"
}

resource "aws_apigatewayv2_route" "photo" {
  api_id    = aws_apigatewayv2_api.photo_gallery.id
  route_key = "DELETE /photos/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.delete_photo.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.photo_gallery.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "api_generate_upload_url" {
  statement_id  = "AllowApiGatewayGenerateUploadUrl"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.generate_upload_url.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.photo_gallery.execution_arn}/*/POST/upload-url"
}

resource "aws_lambda_permission" "api_get_photos" {
  statement_id  = "AllowApiGatewayGetPhotos"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_photos.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.photo_gallery.execution_arn}/*/GET/photos"
}

resource "aws_lambda_permission" "api_delete_photo" {
  statement_id  = "AllowApiGatewayDeletePhoto"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.delete_photo.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.photo_gallery.execution_arn}/*/DELETE/photos/*"
}

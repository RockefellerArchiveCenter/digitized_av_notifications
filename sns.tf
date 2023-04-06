resource "aws_sns_topic" "digitized_av_events" {
    name = "digitized-av-events"
}
resource "aws_sns_topic_policy" "default" {
  arn = aws_sns_topic.digitized_av_events.arn

  policy = data.aws_iam_policy_document.digitized_av_events_topic_policy.json
}

data "aws_iam_policy_document" "digitized_av_events_topic_policy" {
  policy_id = "__default_policy_ID"

  statement {
    actions = [
      "SNS:Subscribe",
      "SNS:SetTopicAttributes",
      "SNS:RemovePermission",
      "SNS:Receive",
      "SNS:Publish",
      "SNS:ListSubscriptionsByTopic",
      "SNS:GetTopicAttributes",
      "SNS:DeleteTopic",
      "SNS:AddPermission",
    ]

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceOwner"

      values = [
        var.account_id,
      ]
    }

    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    resources = [
      aws_sns_topic.digitized_av_events.arn,
    ]

    sid = "__default_statement_ID"
  }
}
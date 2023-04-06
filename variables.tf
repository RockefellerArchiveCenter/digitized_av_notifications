variable "teams_url" {
  type = string
  description = "The URL of an incoming webhook for a Teams channel to which notifications should be posted."
  sensitive = true
}

variable "account_id" {
    type = string
    description = "ARN for organization account"
    sensitive = true
}
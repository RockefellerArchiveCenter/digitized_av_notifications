#!/usr/bin/env python3

import json
import logging
import os

import urllib3

http = urllib3.PoolManager()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def parse_failure_attributes(attributes):
    """Parses message attributes for failure messages."""
    message = attributes['message']['Value']
    color_name = '#ff0000'
    status = attributes['outcome']['Value']
    return message, status, color_name


def send_teams_message(title, message, status, color_name, url):
    """Delivers message to Teams channel endpoint."""
    notification = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": color_name,
        "summary": message,
        "sections": [{
            "activityTitle": title,
            "text": message,
            "facts": [{
                    "name": "Status",
                    "value": status
            }]
        }]}
    encoded_msg = json.dumps(notification).encode('utf-8')
    response = http.request('POST', url, body=encoded_msg)
    logger.info('Status Code: {}'.format(response.status))
    logger.info('Response: {}'.format(response.data))


def lambda_handler(event, context):
    """Main handler for function."""

    attributes = event['Records'][0]['Sns']['MessageAttributes']

    if attributes['outcome']['Value'] == 'FAILURE':
        logger.info("Failure message received.")
        title = event['Records'][0]['Sns']['Message']
        message, status, color_name = parse_failure_attributes(attributes)
        send_teams_message(
            title,
            message,
            status,
            color_name,
            os.environ.get('TEAMS_URL'))
    else:
        logger.info("No status worth notifying.")

#!/usr/bin/env python3

import json
import logging
import os
from base64 import b64decode

import boto3
import urllib3

http = urllib3.PoolManager()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def parse_attributes(attributes):
    """Parses attributes from messages."""
    color_name = '#ff0000' if attributes['outcome']['Value'] == 'FAILURE' else '#008000'
    format = attributes['format']['Value']
    refid = attributes['refid']['Value']
    service = attributes['service']['Value']
    outcome = attributes['outcome']['Value'].lower()
    message = attributes.get('message', {}).get('Value')
    return color_name, format, refid, service, outcome, message


def structure_teams_message(color_name, title, message, facts):
    """Structures Teams message using arguments."""
    notification = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": color_name,
        "summary": message,
        "sections": [{
            "activityTitle": title,
            "text": message,
            "facts": [{"name": k, "value": v} for k, v in facts.items()]
        }]}
    return json.dumps(notification).encode('utf-8')


def send_teams_message(message, url):
    """Delivers message to Teams channel endpoint."""
    response = http.request('POST', url, body=message)
    logger.info('Status Code: {}'.format(response.status))
    logger.info('Response: {}'.format(response.data))


def decrypt_environment_variable(key):
    """Decrypts environment variables."""
    encrypted = os.environ[key]
    return boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(encrypted),
        EncryptionContext={
            'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')


def lambda_handler(event, context):
    """Main handler for function."""
    logger.info("Message received.")

    title = event['Records'][0]['Sns']['Message']
    attributes = event['Records'][0]['Sns']['MessageAttributes']
    color_name, format, refid, service, outcome, message = parse_attributes(
        attributes)
    message = structure_teams_message(
        color_name,
        title,
        message,
        {'Service': service, 'Outcome': outcome, 'Format': format, 'RefID': refid})
    decrypted_url = decrypt_environment_variable('TEAMS_URL')
    send_teams_message(message, decrypted_url)

#!/usr/bin/env python3

import json
from pathlib import Path
from unittest.mock import patch

from src.handle_digitized_av_notifications import lambda_handler

# TODO set environment variable before tests and unset afterwards


@patch('src.handle_digitized_av_notifications.send_teams_message')
def test_success_notification(mock_teams):
    with open(Path('fixtures', 'success_message.json'), 'r') as jf:
        message = json.load(jf)
        lambda_handler(message, None)
        assert mock_teams.call_count == 0


@patch('src.handle_digitized_av_notifications.send_teams_message')
def test_failure_notification(mock_teams):
    with open(Path('fixtures', 'failure_message.json'), 'r') as jf:
        message = json.load(jf)
        lambda_handler(message, None)
        mock_teams.assert_called_once_with(
            'video package 20f8da26e268418ead4aa2365f816a08 failed validation.',
            'BagIt validation failed.',
            'FAILURE',
            '#ff0000',
            None
        )

# TODO make sure notification is correctly formatted

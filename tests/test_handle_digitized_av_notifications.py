#!/usr/bin/env python3

import json
from pathlib import Path
from unittest.mock import patch

from src.handle_digitized_av_notifications import (lambda_handler,
                                                   structure_teams_message)


@patch('src.handle_digitized_av_notifications.structure_teams_message')
@patch('src.handle_digitized_av_notifications.get_config')
@patch('src.handle_digitized_av_notifications.send_teams_message')
def test_success_notification(mock_send, mock_config, mock_structure):
    with open(Path('tests', 'fixtures', 'success_message.json'), 'r') as jf:
        message = json.load(jf)
        lambda_handler(message, None)
        mock_structure.assert_called_once_with(
            '#008000',
            'video package 20f8da26e268418ead4aa2365f816a08 successfully validated.',
            None,
            {'Service': 'validation', 'Outcome': 'success', 'Format': 'video',
                'RefID': '20f8da26e268418ead4aa2365f816a08'}
        )
        mock_config.assert_called_once()
        mock_send.assert_called_once()


@patch('src.handle_digitized_av_notifications.structure_teams_message')
@patch('src.handle_digitized_av_notifications.get_config')
@patch('src.handle_digitized_av_notifications.send_teams_message')
def test_failure_notification(mock_send, mock_config, mock_structure):
    with open(Path('tests', 'fixtures', 'failure_message.json'), 'r') as jf:
        message = json.load(jf)
        lambda_handler(message, None)
        mock_structure.assert_called_once_with(
            '#ff0000',
            'video package 20f8da26e268418ead4aa2365f816a08 failed validation.',
            'BagIt validation failed.',
            {'Service': 'validation', 'Outcome': 'failure', 'Format': 'video',
                'RefID': '20f8da26e268418ead4aa2365f816a08'}
        )
        mock_config.assert_called_once()
        mock_send.assert_called_once()


def test_structure_teams_message():
    for fixture_path, args in [
            ('failure_message_out.json', ['#ff0000', 'video package 20f8da26e268418ead4aa2365f816a08 failed validation.', 'BagIt validation failed.', {'Service': 'validation', 'Outcome': 'failure', 'Format': 'video',
                                                                                                                                                       'RefID': '20f8da26e268418ead4aa2365f816a08'}]),
            ('success_message_out.json', ['#008000', 'video package 20f8da26e268418ead4aa2365f816a08 successfully validated.', None, {'Service': 'validation', 'Outcome': 'success', 'Format': 'video',
                                                                                                                                      'RefID': '20f8da26e268418ead4aa2365f816a08'}])]:
        with open(Path('tests', 'fixtures', fixture_path), 'r') as df:
            expected = json.load(df)
            output = structure_teams_message(*args)
            assert output == json.dumps(expected).encode('utf-8')

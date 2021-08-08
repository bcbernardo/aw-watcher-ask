# SPDX-FileCopyrightText: Bernardo Chrispim Baron <bc.bernardo@hotmail.com>
#
# SPDX-License-Identifier: MIT


"""Tests for aw-watcher-ask main logic."""


from datetime import datetime, timedelta, timezone
from random import randint
from typing import Optional

import pytest
from aw_client import ActivityWatchClient

from aw_watcher_ask.core import (
    _ask_many, _ask_one, _client_setup, _bucket_setup, main
)
from aw_watcher_ask.models import DialogType


def test_client_setup():
    """Tests instantiating an ActivityWatch client object."""
    client = _client_setup(testing=True)
    assert client.client_name == "test-aw-watcher-ask"
    assert client.client_hostname == "localhost.localdomain"
    info = client.get_info()
    assert "hostname" in info
    assert "testing" in info
    with client:
        assert True
    client.connect()
    client.disconnect()


def test_bucket_setup():
    """Tests creating and deleting a bucket"""
    with ActivityWatchClient("test-client", testing=True) as client:

        # create bucket
        new_bucket_id = _bucket_setup(client, question_id="test.question")
        buckets = client.get_buckets()
        assert any(bucket == new_bucket_id for bucket in buckets)

        # delete bucket
        client.delete_bucket(new_bucket_id)
        buckets = client.get_buckets()
        assert not any(bucket == new_bucket_id for bucket in buckets)


def test_ask_question():
    """Tests asking a question with a single answer field to the user."""
    answer = _ask_one(DialogType("question"), "Test question", timeout=2)
    assert "success" in answer
    assert not answer["success"]
    assert "Test question" in answer
    assert len(answer["Test question"]) == 0


def test_ask_many():
    """Tests asking a question with multiple answer fields to the user."""
    with pytest.raises(NotImplementedError):
        _ask_many(DialogType("forms"), timeout=5)


@pytest.mark.parametrize("question_type", ["question"])
@pytest.mark.parametrize("title", ["Test question", None])
def test_main_one(question_type: str, title: Optional[str]):
    """Tests periodically asking a single question and storing user's input."""
    with ActivityWatchClient("test-client", testing=True) as client:
        question_id = "test.question" + str(randint(0, 10 ** 10))
        bucket_id = "test-aw-watcher-ask_localhost.localdomain"
        try:
            start_time = datetime.now(timezone.utc)
            end_time = start_time + timedelta(seconds=9)
            main(
                question_type=DialogType("question"),
                question_id=question_id,
                title=title,
                schedule="* * * * * */4",
                until=end_time,
                timeout=2,
                testing=True,
            )
            last_event = client.get_events(bucket_id=bucket_id, limit=1)[0]
            assert last_event.timestamp > start_time
            assert last_event.timestamp < end_time + timedelta(seconds=2)
            assert "success" in last_event.data
            assert not last_event.data["success"]
            if not title:
                assert question_id in last_event.data
                assert len(last_event.data[question_id]) == 0
            else:
                assert title in last_event.data
                assert len(last_event.data[title]) == 0
        finally:
            client.delete_bucket(bucket_id)

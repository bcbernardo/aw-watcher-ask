# SPDX-FileCopyrightText: Bernardo Chrispim Baron <bc.bernardo@hotmail.com>
#
# SPDX-License-Identifier: MIT


"""Tests for the utilities to interact with Zenity and ActivityWatch."""

import pytest
from datetime import datetime

from aw_watcher_ask.utils import fix_id, is_valid_id, get_current_datetime


@pytest.mark.parametrize("valid_id", ["a.correct.id"])
def testis_valid_id(valid_id: str):
    """Tests recognizing a valid event_type id."""
    assert is_valid_id(valid_id)


@pytest.mark.parametrize(
    "invalid_id",
    [
        "a string with spaces",
        "a_string_with_underscores",
        "ã.string.wïth.nonáscii.çhars",
        "AN.UPPERCASE.STRING",
    ],
)
def test_isnot_valid_id(invalid_id: str):
    """Tests recognizing forbidden event_type ids."""
    assert not is_valid_id(invalid_id)


@pytest.mark.parametrize("valid_id", ["a.correct.id"])
def testfix_valid_id(valid_id: str):
    """Tests applying fix to an already correct event_type id."""
    transformed_id = fix_id(valid_id)
    assert is_valid_id(transformed_id)
    assert valid_id == transformed_id


@pytest.mark.parametrize(
    "invalid_id",
    [
        "a string with spaces",
        "a_string_with_underscores",
        "ã.string.wïth.nonáscii.çhars",
        "AN.UPPERCASE.STRING",
    ],
)
def testfix_invalid_id(invalid_id: str):
    """Tests applying fix to event_type ids with incorrect ."""
    assert is_valid_id(fix_id(invalid_id))


def test_get_current_datetime():
    """Returns the current UTC date and time."""
    now = get_current_datetime()
    assert isinstance(now, datetime)
    assert now.tzname() == "UTC"

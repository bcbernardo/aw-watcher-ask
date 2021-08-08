# SPDX-FileCopyrightText: Bernardo Chrispim Baron <bc.bernardo@hotmail.com>
#
# SPDX-License-Identifier: MIT

"""General utilities for interacting with Zenity and ActivityWatch."""


import re
from datetime import datetime, timezone

from unidecode import unidecode


def fix_id(question_id: str) -> str:
    """Replaces forbidden characters in a question_id."""
    return re.sub(r"[^a-z0-9]", ".", unidecode(question_id).lower())


def is_valid_id(question_id: str) -> bool:
    """Checks whether a given question_id contains only accepted characters."""
    return not bool(re.search(r"[^a-z0-9.]", question_id))


def get_current_datetime() -> datetime:
    """Returns the current UTC date and time."""
    return datetime.now(timezone.utc)

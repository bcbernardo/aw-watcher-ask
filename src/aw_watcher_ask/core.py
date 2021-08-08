# SPDX-FileCopyrightText: Bernardo Chrispim Baron <bc.bernardo@hotmail.com>
#
# SPDX-License-Identifier: MIT


"""Watcher function and helpers."""


import sys
import time
from datetime import datetime
from typing import Any, Dict, Optional

import zenity
from aw_client import ActivityWatchClient
from aw_core.models import Event
from croniter import croniter
from loguru import logger

from aw_watcher_ask.models import DialogType
from aw_watcher_ask.utils import fix_id, is_valid_id, get_current_datetime


def _bucket_setup(client: ActivityWatchClient, question_id: str) -> str:
    """Makes sure a bucket exists in the client for the given event type."""

    bucket_id = "{}_{}".format(client.client_name, client.client_hostname)
    client.create_bucket(bucket_id, event_type=question_id)

    return bucket_id


def _client_setup(testing: bool = False) -> ActivityWatchClient:
    """Builds a new ActivityWatcher client instance and bucket."""

    # set client name
    client_name = "aw-watcher-ask"
    if testing:
        client_name = "test-" + client_name

    # create client representation
    return ActivityWatchClient(client_name, testing=testing)


def _ask_one(
    question_type: DialogType, title: str, *args, **kwargs
) -> Dict[str, Any]:
    """Captures an user's response to a dialog box with a single field."""
    kwargs.pop("ctx", None)
    success, content = zenity.show(
        question_type.value, title=title, *args, **kwargs
    )
    return {
        "success": success,
        title: content,
    }


def _ask_many(
    question_type: DialogType, separator: str = "|", *args, **kwargs
) -> Dict[str, Any]:
    """Captures the user's response to a dialog box with multiple fields."""
    raise NotImplementedError


def main(
    question_id: str,
    question_type: DialogType = DialogType.question,
    title: Optional[str] = None,
    schedule: str = "R * * * *",
    until: datetime = datetime(2100, 12, 31),
    timeout: int = 60,
    testing: bool = False,
    *args,
    **kwargs,
) -> None:
    """Gathers user's inputs and send them to ActivityWatch.

    This watcher periodically presents a dialog box to the user, and stores the
    provided answer on the locally running [ActivityWatch]
    (https://docs.activitywatch.net/) server. It relies on [Zenity]
    (https://help.gnome.org/users/zenity/stable/index.html.en) to construct
    simple graphic interfaces.

    Arguments:
        question_id: A short string to identify your question in ActivityWatch
            server records. Should contain only lower-case letters, numbers and
            dots. If `title` is not provided, this will also be the
            key to identify the content of the answer in the ActivityWatch
            bucket's raw data.
        question_type: The type of dialog box to present the user, provided as
            one of [`aw_watcher_ask.models.DialogType`]
            [aw_watcher_ask.models.DialogType] enumeration types. Currently,
            `DialogType.forms`, `DialogType.list` and
            `DialogType.file_selection` are not supported. Defaults to
            `DialogType.question`.
        title: An optional title for the question. If provided, this
            will be both the title of the dialog box and the key that
            identifies the content of the answer in the ActivityWatch bucket's
            raw data.
        schedule: A [cron-tab expression](https://en.wikipedia.org/wiki/Cron)
            that controls the execution intervals at which the user should be
            prompted to answer the given question. Accepts 'R' as a keyword at
            second, minute and hour positions, for prompting at random times.
            Might be a classic five-element expression, or optionally have a
            sixth element to indicate the seconds.
        until: A [`datetime.datetime`]
            (https://docs.python.org/3/library/datetime.html#datetime-objects)
            object, that indicates the date and time when to stop gathering
            input from the user. Defaults to `datetime(2100, 12, 31)`.
        timeout: The amount of seconds to wait for user's input. Defaults to
            60 seconds.
        testing: Whether to run the [`aw_client.ActivityWatchClient`]
            (https://docs.activitywatch.net/en/latest/api/python.html
            #aw_client.ActivityWatchClient) client in testing mode.
        *args: Variable lenght argument list to be passed to [`zenity.show()`]
            (https://pyzenity.gitbook.io/docs/) Zenity wrapper.
        **kwargs: Variable lenght argument list to be passed to
            [`zenity.show()`](https://pyzenity.gitbook.io/docs/) Zenity
            wrapper.

    Raises:
        NotImplementedError: If the provided `question_type` is one of
            `DialogType.forms`, `DialogType.list` or
            `DialogType.file_selection`.
    """

    log_format = "{time} <{extra[question_id]}>: {level} - {message}"
    logger.add(sys.stderr, level="INFO", format=log_format)
    log = logger.bind(question_id=question_id)

    log.info("Starting new watcher...")

    # fix question-id if it was provided with forbidden characters
    if not is_valid_id(question_id):
        question_id = fix_id(question_id)
        log.warning(
            f"An invalid question_id was provided. Fixed to `{question_id}`."
        )
        log = log.bind(question_id=question_id)

    # fix offset-naive datetimes
    if not until.tzinfo:
        system_timezone = get_current_datetime().astimezone().tzinfo
        until = until.replace(tzinfo=system_timezone)

    # start client and bucket
    client = _client_setup(testing=testing)
    log.info(
        f"Client created and connected to server at {client.server_address}."
    )
    bucket_id = _bucket_setup(client, question_id)

    # execution schedule
    executions = croniter(schedule, start_time=get_current_datetime())

    # run service
    while get_current_datetime() < until:
        # wait until next execution
        next_execution = executions.get_next(datetime)
        log.info(
            f"Next execution scheduled to {next_execution.isoformat()}."
        )
        sleep_time = next_execution - get_current_datetime()
        time.sleep(max(sleep_time.seconds, 0))

        log.info(
            "New prompt fired. Waiting for user input..."
        )
        if question_type.value in ["forms", "file-selection", "list"]:
            # TODO: not implemented
            answer = _ask_many(
                question_type=question_type,
                title=title,
                timeout=timeout,
                *args,
                **kwargs,
            )
        else:
            answer = _ask_one(
                question_type=question_type,
                title=(
                    title if title else question_id
                ),
                timeout=timeout,
                *args,
                **kwargs,
            )
        if not answer["success"]:
            log.info("Prompt timed out with no response from user.")

        event = Event(timestamp=get_current_datetime(), data=answer)
        client.insert_event(bucket_id, event)
        log.info(f"Event stored in bucket '{bucket_id}'.")

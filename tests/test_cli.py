# SPDX-FileCopyrightText: Bernardo Chrispim Baron <bc.bernardo@hotmail.com>
#
# SPDX-License-Identifier: MIT


"""Tests running aw-watcher-input from the command-line interface."""


import re
from datetime import datetime, timedelta

import pytest
from typer.testing import CliRunner

from aw_watcher_ask.cli import app


@pytest.fixture(scope="function")
def runner():
    """Provides a command-line test runner."""
    return CliRunner()


def test_version(runner):
    """Tests getting app version."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert re.match(r"[0-9]+\.[0-9]+\.[0-9]+", result.stdout)


@pytest.mark.parametrize("question_id", ["accepted.id", "Forbiddên_ID"])
@pytest.mark.parametrize("question_type", ["question", "entry"])
@pytest.mark.parametrize("schedule", ["* * * * * */4"])
def test_app(runner, question_id, question_type, schedule):
    end_time = datetime.now() + timedelta(seconds=9)
    result = runner.invoke(
        app,
        [
            "run",
            question_type,
            "--testing",
            "--id",
            question_id,
            "--schedule",
            schedule,
            "--until",
            end_time.isoformat(timespec="seconds"),
            "--timeout",
            2,
        ],
    )
    assert result.exit_code == 0
    assert "INFO - Starting new watcher" in result.output
    assert "INFO - Client created" in result.output
    assert "INFO - Next execution scheduled" in result.output
    assert "INFO - New prompt fired" in result.output
    assert "INFO - Prompt timed out" in result.output
    assert "INFO - Event stored in bucket" in result.output

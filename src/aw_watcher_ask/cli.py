# SPDX-FileCopyrightText: Bernardo Chrispim Baron <bc.bernardo@hotmail.com>
#
# SPDX-License-Identifier: MIT


"""A command-line interface (CLI) to aw-watcher-ask."""


from datetime import datetime
from typing import Dict, List, Optional, Union

import typer

from aw_watcher_ask import __version__
from aw_watcher_ask.core import main
from aw_watcher_ask.models import DialogType


app = typer.Typer()


def _parse_extra_args(
    extra_args: List[str]
) -> Dict[str, Union[bool, str, List[str]]]:
    """Processes any number of unknown CLI arguments and/or options.

    Arguments:
        extra_args: A list of unprocessed arguments and/or options forwarded
            by a Click/Typer command-line application.

    Returns:
        A dictionary of option names and values.
    """

    options: Dict[str, Union[bool, str, List[str]]] = dict()

    # iterate over unparsed options
    for ix in range(0, len(extra_args)):

        # check whether the element in this position starts with an option name
        if extra_args[ix].startswith("-"):

            # if it is, remove it from un parsed args and split the option name
            # and an optional value (if format `--name=value` was used)
            option_name, *option_values = extra_args[ix].split("=", 1)
            option_name = option_name.lstrip("-")

            if not option_values:
                # no value in `=`-separated value: keep parsing for
                # (possibly multiple) values, provided in the format
                # `--name option1 option 2`
                while True:
                    if extra_args[ix].startswith("-"):
                        # found the next option name; stop looking for values
                        break
                    else:
                        # is a value; remove it from unparsed args and store it
                        option_values.append(extra_args[ix])

            # have any value been found?
            if len(option_values) == 0:
                # no: assume option was a flag, and store True
                options[option_name] = True
            elif len(option_values) == 1:
                # yes, one value has been found: unpack it and store it
                options[option_name] = option_values[0]
            else:
                # multiple values have been found: store them as a list
                options[option_name] = option_values

    return options


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        False, "--version", help="Show program version.", show_default=False
    ),
):
    """Gathers user's inputs and send them to ActivityWatch.

    This watcher periodically presents a dialog box to the user, and stores the
    provided answer on the locally running ActivityWatch server. It relies on
    Zenity to construct simple graphic interfaces.
    """
    if version and ctx.invoked_subcommand is None:
        typer.echo(__version__)
        typer.Exit()


@app.command(context_settings={
    "allow_extra_args": True,
    "ignore_unknown_options": True,
    "allow_interspersed_args": False,
})
def run(
    ctx: typer.Context,
    question_type: DialogType = typer.Option(..., help=(
        "The type of dialog box to present the user."
    )),
    question_id: str = typer.Option(..., help=(
        "A short string to identify your question in ActivityWatch "
        "server records. Should contain only lower-case letters, numbers and "
        "dots. If `--title` is not provided, this will also be the "
        "key to identify the content of the answer in the ActivityWatch "
        "bucket's raw data."
    )),
    title: Optional[str] = typer.Option(None, help=(
        "An optional title for the question. If provided, this will be both "
        "the title of the dialog box and the key that identifies the content "
        "of the answer in the ActivityWatch bucket's raw data."
    )),
    schedule: str = typer.Option("R * * * *", help=(
        "A cron-tab expression (see https://en.wikipedia.org/wiki/Cron) "
        "that controls the execution intervals at which the user should be "
        "prompted to answer the given question. Accepts 'R' as a keyword at "
        "second, minute and hour positions, for prompting at random times."
        "Might be a classic five-element expression, or optionally have a "
        "sixth element to indicate the seconds."
    )),
    until: datetime = typer.Option("2100-12-31", help=(
        "A date and time when to stop gathering input from the user."
    )),
    timeout: int = typer.Option(
        60, help="The amount of seconds to wait for user's input."
    ),
    testing: bool = typer.Option(
        False, help="If set, starts ActivityWatch Client in testing mode."
    ),
):
    params = locals().copy()
    params.pop("ctx", None)
    params = dict(params, **_parse_extra_args(ctx.args))
    main(**params)

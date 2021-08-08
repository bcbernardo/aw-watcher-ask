# SPDX-FileCopyrightText: Bernardo Chrispim Baron <bc.bernardo@hotmail.com>
#
# SPDX-License-Identifier: MIT

"""Representations for exchanging data with Zenity and ActivityWatch."""


from enum import Enum


class DialogType(str, Enum):
    calendar = "calendar"  # Display calendar dialog
    entry = "entry"  # Display text entry dialog
    error = "error"  # Display error dialog
    info = "info"  # Display info dialog
    file_selection = "file-selection"  # Display file selection dialog
    list = "list"  # Display list dialog
    notification = "notification"  # Display notification
    progress = "progress"  # Display progress indication dialog
    warning = "warning"  # Display warning dialog
    scale = "scale"  # Display scale dialog
    text_info = "text-info"  # Display text information dialog
    color_selection = "color-selection"  # Display color selection dialog
    question = "question"  # Display question dialog
    password = "password"  # Display password dialog
    forms = "forms"  # Display forms dialog

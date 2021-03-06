"""nextcloud-notes-api is an unofficial wrapper for the
    [Nextcloud Notes app](https://github.com/nextcloud/notes) API

    .. include:: documentation.md
    """

from .api_exceptions import (
    InsufficientNextcloudStorage,
    InvalidNextcloudCredentials,
    InvalidNoteId,
    NoteNotFound,
)
from .api_wrapper import NotesApi
from .note import Note

__version__ = '0.1.0'
__all__ = [
    'InsufficientNextcloudStorage',
    'InvalidNextcloudCredentials',
    'InvalidNoteId',
    'NoteNotFound',
    'NotesApi',
    'Note',
]

from .note import Note
from .api_wrapper import NotesApi
from .api_exceptions import (
    InsufficientNextcloudStorage,
    InvalidNextcloudCredentials,
    InvalidNoteId,
    NoteNotFound,
)

__version__ = '0.1.0'

from .note import Note


class NotesApiError(Exception):
    """All NotesApi Exceptions inherit from this class"""

    def __init__(self, msg='', *_, **kwargs):
        self.msg = (
            msg +
            ', '.join(f'{key}="{val}"' for key, val in kwargs.items())
        )

    def __str__(self):
        return self.msg


class InvalidNextcloudCredentials(NotesApiError):
    """Supplied credentials are invalid"""

    def __init__(self, username: str, password: str, hostname: str):
        NotesApiError.__init__(
            self,
            'Invalid credentials: ',
            username=username,
            password=password,
            hostname=hostname
        )


class InvalidNoteId(NotesApiError):
    """Requested note id is invalid"""

    def __init__(self, note_id: int, hostname: str):
        NotesApiError.__init__(
            self,
            'Invalid note id: ',
            note_id=note_id,
            hostname=hostname
        )


class NoteNotFound(NotesApiError):
    """Note doesn't exist"""

    def __init__(self, note_id: int, hostname: str):
        NotesApiError.__init__(
            self,
            'Note not found: ',
            note_id=note_id,
            hostname=hostname
        )


class InsufficientNextcloudStorage(NotesApiError):
    """Not enough free storage for saving the notes content"""

    def __init__(self, hostname: str, note: Note):
        NotesApiError.__init__(
            self,
            'Not enough free space for saving note: ',
            hostname=hostname,
            note=note
        )

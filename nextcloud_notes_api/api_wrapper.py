from copy import deepcopy
from dataclasses import dataclass, field
from typing import Iterator, List, Sequence, Tuple, Union

from requests import delete, get, post, put

from .api_exceptions import (
    InsufficientNextcloudStorage,
    InvalidNextcloudCredentials,
    InvalidNoteId,
    NoteNotFound,
)
from .note import Note


class NotesApi:
    """Wraps the [Nextcloud Notes app API](https://github.com/nextcloud/notes/blob/master/docs/api/v1.md)."""  # noqa: E501

    @dataclass
    class EtagCache:
        """Convenience class for caching notes using HTTP ETags."""

        etag: str = ''
        notes: List[Note] = field(default_factory=list)

    def __init__(
        self, username: str, password: str, hostname: str, *, etag_caching: bool = True
    ):
        """
        Args:
            username (str): Nextcloud username.
            password (str): Nextcloud password.
            hostname (str): Nextcloud hostname.
            etag_caching (bool, optional): Whether to cache notes using HTTP ETags, if
                the server supports it. Defaults to True.
        """
        self.username = username
        """`str`: Nextcloud username."""
        self.password = password
        """`str`: Nextcloud password."""
        self.hostname = hostname
        """`str`: Nextcloud hostname."""
        self.etag_caching = etag_caching
        """`bool`: Whether to cache notes using HTTP ETags."""

        self._etag_cache = NotesApi.EtagCache()
        self._common_headers = {'OCS-APIRequest': 'true', 'Accept': 'application/json'}

    @property
    def auth_pair(self) -> Tuple[str, str]:
        """Tuple[str, str]: Tuple of `NotesApi.username` and `NotesApi.password`."""
        return (self.username, self.password)

    def get_api_version(self) -> str:
        """
        Returns:
            str: Highest supported Notes app api version.
        """
        response = get(
            f'https://{self.hostname}/ocs/v2.php/cloud/capabilities',
            auth=self.auth_pair,
            headers=self._common_headers,
        )

        return response.json()['ocs']['data']['capabilities']['notes']['api_version'][
            -1
        ]

    def get_all_notes(self) -> Union[Iterator[Note], Sequence[Note]]:
        """Fetch all notes.

        Returns:
            Union[Iterator[Note], Sequence[Note]]: A `typing.Iterator` or
                `collections.abc.Sequence` of all notes.

        Raises:
            InvalidNextcloudCredentials: Invalid credentials supplied.
        """
        headers = self._common_headers
        if self.etag_caching:
            headers['If-None-Match'] = self._etag_cache.etag

        response = get(
            f'https://{self.hostname}/index.php/apps/notes/api/v1/notes',
            auth=self.auth_pair,
            headers=headers,
        )

        if response.status_code == 401:
            raise InvalidNextcloudCredentials(
                self.username, self.password, self.hostname
            )

        # Cache is valid
        if response.status_code == 304 and self.etag_caching:
            return self._etag_cache.notes

        if self.etag_caching:
            notes = [Note(**note_dict) for note_dict in response.json()]
            # Update cache
            self._etag_cache = NotesApi.EtagCache(
                response.headers['ETag'], deepcopy(notes)
            )
            return notes
        else:
            return (Note(**note_dict) for note_dict in response.json())

    def get_single_note(self, note_id: int) -> Note:
        """Retrieve note with ID `note_id`.

        Args:
            note_id (int): ID of note to retrieve.

        Returns:
            Note: Note with id `note_id`.

        Raises:
            InvalidNoteId: `note_id` is an invalid ID.
            InvalidNextcloudCredentials: Invalid credentials supplied.
            NoteNotFound: Note with id `note_id` doesn't exist.
        """
        response = get(
            f'https://{self.hostname}/index.php/apps/notes/api/v1/notes/{note_id}',
            auth=self.auth_pair,
            headers=self._common_headers,
        )

        if response.status_code == 400:
            raise InvalidNoteId(note_id, self.hostname)
        elif response.status_code == 401:
            raise InvalidNextcloudCredentials(
                self.username, self.password, self.hostname
            )
        elif response.status_code == 404:
            raise NoteNotFound(note_id, self.hostname)

        return Note(**response.json())

    def create_note(self, note: Note) -> Note:
        """Create new note.

        `Note.id` and `Note.modified` are set by the server.
        `Note.title` will also be changed in case there already is a note with the same
        title, e.g. 'Todo' -> 'Todo (2)'.

        Args:
            note (Note): Note to create.

        Returns:
            Note: Created note with `Note.id` and `Note.modified` set.

        Raises:
            InvalidNextcloudCredentials: Invalid credentials supplied.
            InsufficientNextcloudStorage: Not enough storage to save `note`.
        """
        response = post(
            f'https://{self.hostname}/index.php/apps/notes/api/v1/notes',
            auth=self.auth_pair,
            headers=self._common_headers,
            data=note.to_dict(),
        )

        # Getting a status 400 is impossible since the note id is ignored by the
        # server, although specified by the api docs
        if response.status_code == 401:
            raise InvalidNextcloudCredentials(
                self.username, self.password, self.hostname
            )
        elif response.status_code == 507:
            raise InsufficientNextcloudStorage(self.hostname, note)

        return Note(**response.json())

    def update_note(self, note: Note) -> Note:
        """Update `note`.

        Args:
            note (Note): New note, `Note.id` has to match the ID of the note to be
                replaced.

        Returns:
            Note: Updated note with new `Note.modified`.

        Raises:
            ValueError: `Note.id` is not set.
            InvalidNoteId: `Note.id` is an invalid ID.
            InvalidNextcloudCredentials: Invalid credentials supplied.
            NoteNotFound: Note with id `Note.id` doesn't exist.
            InsufficientNextcloudStorage: Not enough storage to save `note`.
        """
        if not note.id:
            raise ValueError(f'Note id not set {note}')

        data = note.to_dict()
        del data['id']

        response = put(
            f'https://{self.hostname}/index.php/apps/notes/api/v1/notes/{note.id}',
            auth=self.auth_pair,
            headers=self._common_headers,
            data=data,
        )

        if response.status_code == 400:
            raise InvalidNoteId(note.id, self.hostname)
        elif response.status_code == 401:
            raise InvalidNextcloudCredentials(
                self.username, self.password, self.hostname
            )
        elif response.status_code == 404:
            raise NoteNotFound(note.id, self.hostname)
        elif response.status_code == 507:
            raise InsufficientNextcloudStorage(self.hostname, note)

        return Note(**response.json())

    def delete_note(self, note_id: int):
        """Delete note with ID `note_id`.

        Args:
            note_id (int): ID of note to delete

        Raises:
            InvalidNoteId: `note_id` is an invalid ID.
            InvalidNextcloudCredentials: Invalid credentials supplied.
            NoteNotFound: Note with id `note_id` doesn't exist.
        """
        response = delete(
            f'https://{self.hostname}/index.php/apps/notes/api/v1/notes/{note_id}',
            auth=self.auth_pair,
            headers=self._common_headers,
        )

        if response.status_code == 400:
            raise InvalidNoteId(note_id, self.hostname)
        elif response.status_code == 401:
            raise InvalidNextcloudCredentials(
                self.username, self.password, self.hostname
            )
        elif response.status_code == 404:
            raise NoteNotFound(note_id, self.hostname)

    def __repr__(self):
        return f'<NotesApi [{self.hostname}]>'

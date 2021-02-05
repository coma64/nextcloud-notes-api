from requests import get, post, put, delete
from typing import Tuple, List, Iterator, Union
from dataclasses import dataclass, field
from copy import deepcopy

from .note import Note
from .api_exceptions import (
    InsufficientNextcloudStorage,
    InvalidNextcloudCredentials,
    InvalidNoteId,
    NoteNotFound
)


class NotesApi:
    """Wraps the Nextcloud Notes App api

    https://github.com/nextcloud/notes/blob/master/docs/api/v1.md
    """
    @dataclass
    class EtagCache:
        """Convenience class for caching notes using http etags"""
        etag: str = ''
        notes: List[Note] = field(default_factory=list)

    def __init__(self, username: str, password: str, hostname: str, *, etag_caching: bool = True):
        """
        Args:
            username (str): Username
            password (str): Password
            hostname (str): Hostname, e. g. `google.com`
            etag_caching (bool, optional): Whether to cache notes using http etags, if the server
                supports it. Defaults to True.
        """
        self.username = username
        """str: Username"""
        self.password = password
        """str: Password"""
        self.hostname = hostname
        """str: Hostname"""
        self.etag_caching = etag_caching
        """bool: Whether to cache notes using http etags"""

        self._etag_cache = NotesApi.EtagCache()
        self.common_headers = {
            'OCS-APIRequest': 'true',
            'Accept': 'application/json'
        }

    @property
    def auth_pair(self) -> Tuple[str]:
        """Tuple[str]: Tuple of `NotesApi.username` and `NotesApi.password`"""
        return (self.username, self.password)

    def get_api_version(self) -> str:
        """
        Returns:
            str: Highest supported Notes app api version by Nextcloud server
        """
        response = get(
            f'https://{self.hostname}/ocs/v2.php/cloud/capabilities', auth=self.auth_pair, headers=self.common_headers
        )

        return response.json()['ocs']['data']['capabilities']['notes']['api_version'][-1]

    def get_all_notes(self) -> Union[Iterator[Note], List[Note]]:
        """Get all notes

        Returns:
            Union[Iterator[Note], List[Note]]: A list or iterator of all notes

        Raises:
            InvalidNextcloudCredentials: Invalid credentials
        """
        headers = self.common_headers
        if self.etag_caching:
            headers['If-None-Match'] = self._etag_cache.etag

        response = get(
            f'https://{self.hostname}/index.php/apps/notes/api/v1/notes', auth=self.auth_pair, headers=headers
        )

        if response.status_code == 200 and self.etag_caching:
            notes = list(map(Note.from_dict, response.json()))
            # Update cache
            self._etag_cache = NotesApi.EtagCache(
                response.headers['ETag'],
                deepcopy(notes)
            )
            return notes
        elif response.status_code == 200 and not self.etag_caching:
            return map(Note.from_dict, response.json())
        elif response.status_code == 304 and self.etag_caching:
            # Cache valid
            return self._etag_cache.notes
        elif response.status_code == 401:
            raise InvalidNextcloudCredentials(
                self.username,
                self.password,
                self.hostname
            )

    def get_single_note(self, note_id: int) -> Note:
        """Get note with id `note_id`

        Args:
            note_id (int): Which note to get

        Returns:
            Note: Note with id `note_id`

        Raises:
            InvalidNoteId: `note_id` invalid
            InvalidNextcloudCredentials: Credentials invalid
            NoteNotFound: Note with id `note_id` doesn't exist
        """
        response = get(
            f'https://{self.hostname}/index.php/apps/notes/api/v1/notes/{note_id}', auth=self.auth_pair, headers=self.common_headers
        )

        if response.status_code == 200:
            return Note.from_dict(response.json())
        elif response.status_code == 400:
            raise InvalidNoteId(note_id, self.hostname)
        elif response.status_code == 401:
            raise InvalidNextcloudCredentials(
                self.username, self.password, self.hostname)
        elif response.status_code == 404:
            raise NoteNotFound(note_id, self.hostname)

    def create_note(self, note: Note) -> Note:
        """Create new note

        `note.id` and `note.modified` are set by the server

        Args:
            note (Note): Note to create

        Returns:
            Note: Created note with `note.id` and `note.modified` set

        Raises:
            InvalidNoteId: `note.id` invalid - don't actually know the purpose of this
            InvalidNextcloudCredentials: Credentials invalid
            InsufficientNextcloudStorage: Not enough storage to save `note`
        """
        data = note.to_dict()
        if 'id' in data:
            del data['id']

        response = post(
            f'https://{self.hostname}/index.php/apps/notes/api/v1/notes', auth=self.auth_pair, headers=self.common_headers, data=data
        )

        if response.status_code == 200:
            return Note.from_dict(response.json())
        elif response.status_code == 400:
            raise InvalidNoteId(note.id, self.hostname)
        elif response.status_code == 401:
            raise InvalidNextcloudCredentials(
                self.username, self.password, self.hostname)
        elif response.status_code == 507:
            raise InsufficientNextcloudStorage(self.hostname, note)

    def update_note(self, note: Note) -> Note:
        """Update `note` 

        Args:
            note (Note): New note, `note.id` has to be the id of the note to be replaced

        Returns:
            Note: Updated note with new `note.modified`

        Raises:
            ValueError: `note.id` not set
            InvalidNoteId: `note.id` invalid
            InvalidNextcloudCredentials: Credentials invalid
            NoteNotFound: Note with id `note.id` doesn't exist
            InsufficientNextcloudStorage: Not enough storage to save `note`
        """
        if not note.id:
            raise ValueError(f'Note id not set {note}')

        data = note.to_dict()
        del data['id']

        response = put(
            f'https://{self.hostname}/index.php/apps/notes/api/v1/notes/{note.id}', auth=self.auth_pair, headers=self.common_headers, data=data
        )

        if response.status_code == 200:
            return Note.from_dict(response.json())
        elif response.status_code == 400:
            raise InvalidNoteId(note.id, self.hostname)
        elif response.status_code == 401:
            raise InvalidNextcloudCredentials(
                self.username,
                self.password,
                self.hostname
            )
        elif response.status_code == 404:
            raise NoteNotFound(note.id, self.hostname)
        elif response.status_code == 507:
            raise InsufficientNextcloudStorage(self.hostname, note)

    def delete_note(self, note_id: int):
        """Delete note with id `note_id`

        Args:
            note_id (int): Id of note to delete

        Raises:
            InvalidNoteId: `note_id` invalid
            InvalidNextcloudCredentials: Credentials invalid
            NoteNotFound: Note with id `note_id` doesn't exist
        """
        response = delete(
            f'https://{self.hostname}/index.php/apps/notes/api/v1/notes/{note_id}',
            auth=self.auth_pair,
            headers=self.common_headers
        )

        if response.status_code == 400:
            raise InvalidNoteId(note_id, self.hostname)
        elif response.status_code == 401:
            raise InvalidNextcloudCredentials(
                self.username,
                self.password,
                self.hostname
            )
        elif response.status_code == 404:
            raise NoteNotFound(note_id, self.hostname)

    def __repr__(self):
        return f'<NotesApi [{self.hostname}]>'

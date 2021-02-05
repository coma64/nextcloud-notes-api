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
    @dataclass
    class EtagCache:
        etag: str = ''
        notes: List[Note] = field(default_factory=list)

    def __init__(self, username: str, password: str, hostname: str, *, etag_caching: bool = True):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.etag_caching = etag_caching

        self._etag_cache = NotesApi.EtagCache()
        self.common_headers = {
            'OCS-APIRequest': 'true',
            'Accept': 'application/json'
        }

    @property
    def auth_pair(self) -> Tuple[str]: return (self.username, self.password)

    def get_api_version(self) -> str:

        response = get(
            f'https://{self.hostname}/ocs/v2.php/cloud/capabilities', auth=self.auth_pair, headers=self.common_headers
        )

        return response.json()['ocs']['data']['capabilities']['notes']['api_version'][-1]

    def get_all_notes(self) -> Union[Iterator[Note], List[Note]]:
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

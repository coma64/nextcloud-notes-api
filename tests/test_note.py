import pytest
from datetime import datetime

import nextcloud_notes_api
from nextcloud_notes_api import Note


class DatetimeNowMock:
    def __init__(self, dt: datetime):
        self.dt = dt

    def now(self) -> datetime:
        return self.dt

    def fromtimestamp(self, timestamp: float) -> datetime:
        return datetime.fromtimestamp(timestamp)


def test_note_generate_modified(monkeypatch):
    dt = datetime.now()
    monkeypatch.setattr(nextcloud_notes_api.note, 'datetime', DatetimeNowMock(dt))
    note = Note(generate_modified=True)

    assert note.modified == dt


def test_note_init():
    note_dict = {
        'title': 'Spam',
        'content': 'Bacon',
        'category': 'Todo',
        'favorite': True,
        'id': 1337,
        'modified': 90_000,
    }

    note = Note(**note_dict)
    assert note_dict == note.to_dict()


def test_note_init_modified_datetime():
    dt = datetime.now()
    note_dict = {
        'title': 'Spam',
        'content': 'Bacon',
        'category': 'Todo',
        'favorite': True,
        'id': 1337,
        'modified': 90_000,
        'modified_datetime': dt,
    }
    # modified should be set to modified_datetime and not modified
    note = Note(**note_dict)
    assert note.modified == dt


def test_note_init_unused_kwargs():
    note_dict = {
        'title': 'Spam',
        'content': 'Bacon',
        'category': 'Todo',
        'favorite': True,
        'id': 1337,
        'modified': 90_000,
        'unused kwarg': 324,
    }

    note = Note(**note_dict)
    del note_dict['unused kwarg']
    assert note_dict == note.to_dict()


def test_note_to_dict():
    note_dict = {
        'title': 'todo',
        'content': 'buy potatoes',
        'category': 'important',
        'favorite': True,
        'id': 1337,
        'modified': 90_000,
    }

    note = Note(**note_dict)
    assert note_dict == note.to_dict()


def test_note_update_modified(random_note: Note, monkeypatch):
    dt = datetime.now()
    monkeypatch.setattr(nextcloud_notes_api.note, 'datetime', DatetimeNowMock(dt))

    random_note.update_modified()

    assert random_note.modified == dt


def test_note_update_modified_user_timestamp(random_note: Note):
    dt = datetime.now()

    random_note.update_modified(dt)

    assert random_note.modified == dt


def test_note_repr(random_note: Note):
    assert repr(random_note) == f'<Note [{random_note.id}]>'


def test_note_str():
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=90_000,
    )

    assert (
        str(note)
        == f"Note[{{'title': 'todo', 'content': 'buy potatoes', 'category': 'important', 'favorite': True, 'id': 1337, 'modified': '{str(note.modified)}'}}]"
    )


def test_note_str_empty_note():
    note = Note()

    assert (
        str(note)
        == "Note[{'title': '', 'content': '', 'category': '', 'favorite': False, 'id': None, 'modified': None}]"
    )

import pytest
from datetime import datetime

import nextcloud_notes_api
from nextcloud_notes_api import Note


class DatetimeNowMock:
    def __init__(self, dt: datetime):
        self.dt = dt

    def now(self) -> datetime:
        return self.dt


def test_note_generate_modified(monkeypatch):
    dt = datetime.now()
    monkeypatch.setattr(
        nextcloud_notes_api.note,
        'datetime',
        DatetimeNowMock(dt)
    )
    note = Note('', '', generate_modified=True)

    assert note.modified == dt.timestamp()


def test_note_from_dict():
    note_dict = {
        'title': 'todo',
        'content': 'buy potatoes',
        'category': 'important',
        'favorite': True,
        'id': 1337,
        'modified': 1234
    }
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=1234
    )

    assert note == Note.from_dict(note_dict)


def test_note_from_dict_empty_note():
    note_dict = {}
    Note.from_dict(note_dict)


def test_note_from_dict_too_many_elements():
    note_dict = {
        'title': 'todo',
        'content': 'buy potatoes',
        'category': 'important',
        'favorite': True,
        'id': 1337,
        'modified': 1234,
        'error': False,
        'errorMessage': ''
    }
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=1234
    )

    assert note == Note.from_dict(note_dict)


def test_note_from_dict_generate_modified():
    note_dict = {
        'title': 'todo',
        'content': 'buy potatoes',
    }

    assert Note.from_dict(note_dict, generate_modified=True).modified


def test_note_to_dict():
    note_dict = {
        'title': 'todo',
        'content': 'buy potatoes',
        'category': 'important',
        'favorite': True,
        'id': 1337,
        'modified': 1234
    }

    note = Note.from_dict(note_dict)
    assert note_dict == note.to_dict()


def test_note_update_modified(monkeypatch):
    dt = datetime.now()
    monkeypatch.setattr(
        nextcloud_notes_api.note,
        'datetime',
        DatetimeNowMock(dt)
    )

    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=1234
    )
    note.update_modified()

    assert note.modified == dt.timestamp()


def test_note_modified_to_datetime():
    dt = datetime.now()
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=dt.timestamp()
    )

    assert dt == note.modified_to_datetime()


def test_note_modified_to_str():
    dt = datetime.now()
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=dt.timestamp()
    )

    assert note.modified_to_str() == dt.strftime('%Y-%m-%d %H:%M:%S')


def test_note_repr():
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=1234
    )

    assert (
        repr(note) ==
        "<Note [1337]>"
    )


def test_note_str():
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=1234
    )

    assert (
        str(note) ==
        f"Note[{{'title': 'todo', 'content': 'buy potatoes', 'category': 'important', 'favorite': True, 'id': 1337, 'modified': '{note.modified_to_str()}'}}]"
    )


def test_note_str_empty_note():
    note = Note()

    assert (
        str(note) == "Note[{'title': '', 'content': '', 'category': '', 'favorite': False, 'id': None, 'modified': None}]"
    )

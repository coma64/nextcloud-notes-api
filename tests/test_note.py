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
    monkeypatch.setattr(nextcloud_notes_api.note, 'datetime', DatetimeNowMock(dt))
    note = Note(generate_modified=True)

    assert note.modified == dt.timestamp()


def test_note_init():
    note_dict = {
        'title': 'Spam',
        'content': 'Bacon',
        'category': 'Todo',
        'favorite': True,
        'id': 1337,
        'modified': 1234,
    }

    note = Note(**note_dict)
    assert note_dict == note.to_dict()


def test_note_init_unused_kwargs():
    note_dict = {
        'title': 'Spam',
        'content': 'Bacon',
        'category': 'Todo',
        'favorite': True,
        'id': 1337,
        'modified': 1234,
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
        'modified': 1234,
    }

    note = Note(**note_dict)
    assert note_dict == note.to_dict()


def test_note_update_modified(monkeypatch):
    dt = datetime.now()
    monkeypatch.setattr(nextcloud_notes_api.note, 'datetime', DatetimeNowMock(dt))

    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=1234,
    )
    note.update_modified()

    assert note.modified == dt.timestamp()


def test_note_update_modified_user_timestamp(monkeypatch):
    dt = datetime.now()

    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=1234,
    )
    note.update_modified(dt)

    assert note.modified == dt.timestamp()


def test_note_modified_to_datetime():
    dt = datetime.now()
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=dt.timestamp(),
    )

    assert dt == note.modified_to_datetime()


def test_note_modified_to_datetime_raises_modified_not_set():
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
    )
    with pytest.raises(ValueError):
        note.modified_to_datetime()


def test_note_modified_to_str():
    dt = datetime.now()
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=dt.timestamp(),
    )

    assert note.modified_to_str() == dt.strftime('%Y-%m-%d %H:%M:%S')


def test_note_modified_to_str_raises_modified_not_set():
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
    )

    with pytest.raises(ValueError):
        note.modified_to_str()


def test_note_repr():
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=1234,
    )

    assert repr(note) == "<Note [1337]>"


def test_note_str():
    note = Note(
        'todo',
        'buy potatoes',
        category='important',
        favorite=True,
        id=1337,
        modified=1234,
    )

    assert (
        str(note)
        == f"Note[{{'title': 'todo', 'content': 'buy potatoes', 'category': 'important', 'favorite': True, 'id': 1337, 'modified': '{note.modified_to_str()}'}}]"
    )


def test_note_str_empty_note():
    note = Note()

    assert (
        str(note)
        == "Note[{'title': '', 'content': '', 'category': '', 'favorite': False, 'id': None, 'modified': None}]"
    )

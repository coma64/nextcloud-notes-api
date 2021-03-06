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


def test_note_update_modified(example_note: Note, monkeypatch):
    dt = datetime.now()
    monkeypatch.setattr(nextcloud_notes_api.note, 'datetime', DatetimeNowMock(dt))

    example_note.update_modified()

    assert example_note.modified == dt


def test_note_update_modified_user_timestamp(example_note: Note):
    dt = datetime.now()

    example_note.update_modified(dt)

    assert example_note.modified == dt


def test_note_repr(example_note: Note):
    assert repr(example_note) == f'<Note [{example_note.id}]>'


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
        == f"Note[{{'title': 'todo', 'content': 'buy potatoes', 'category': 'important', 'favorite': True, 'id': 1337, 'modified': '{str(note.modified)}'}}]"  # noqa: E501
    )


def test_note_str_empty_note():
    note = Note()

    assert (
        str(note)
        == "Note[{'title': None, 'content': None, 'category': None, 'favorite': None, 'id': None, 'modified': None}]"  # noqa: E501
    )

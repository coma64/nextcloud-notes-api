import pytest
from datetime import datetime

from nextcloud_notes_api import Note


def test_note_raises_if_no_modified_passed():
    with pytest.raises(Exception):
        Note(1337, 'ham', 'spam', '', False)


def test_note_generate_modified():
    note = Note(1337, 'ham', 'spam', '', False, generate_modified=True)

    assert note.modified


def test_note_from_dict():
    note_dict = {
        'id': 1337,
        'title': 'spam',
        'modified': 1234,
        'category': '',
        'favorite': False,
        'content': 'ham'
    }
    note = Note(1337, 'ham', 'spam', '', False, 1234)

    assert note == Note.from_dict(note_dict)


def test_note_from_dict_raises_too_few_elements():
    note_dict = {
        'id': 1337,
        'title': 'spam',
        'modified': 1234,
        'category': '',
        'content': 'ham'
    }

    with pytest.raises(Exception):
        Note.from_dict(note_dict)


def test_note_from_dict_too_many_elements():
    note_dict = {
        'id': 1337,
        'title': 'spam',
        'modified': 1234,
        'category': '',
        'favorite': False,
        'error': False,
        'errorMessage': '',
        'content': 'ham'
    }
    note = Note(1337, 'ham', 'spam', '', False, 1234)

    assert note == Note.from_dict(note_dict)


def test_note_from_dict_generate_modified():
    note_dict = {
        'id': 1337,
        'title': 'spam',
        'category': '',
        'favorite': False,
        'content': 'ham'
    }

    assert Note.from_dict(note_dict, generate_modified=True).modified


def test_note_to_dict():
    note_dict = {
        'id': 1337,
        'title': 'spam',
        'category': '',
        'favorite': False,
        'content': 'ham',
        'modified': 1234
    }
    note = Note.from_dict(note_dict)

    assert note_dict == note.to_dict()


def test_note_to_dict_omit_modified():
    note_dict = {
        'id': 1337,
        'title': 'spam',
        'category': '',
        'favorite': False,
        'content': 'ham',
        'modified': 1234
    }
    note = Note.from_dict(note_dict)
    note_dict.pop('modified')

    assert note_dict == note.to_dict(omit_modified=True)


def test_note_to_dict_update_modified():
    note_dict = {
        'id': 1337,
        'title': 'spam',
        'category': '',
        'favorite': False,
        'content': 'ham',
        'modified': 1234
    }
    note = Note.from_dict(note_dict)

    assert (note_dict['modified'] !=
            note.to_dict(update_modified=True)['modified'])


def test_note_update_modified():
    note = Note(1337, 'ham', 'spam', '', False, 1234)
    dt = datetime.now()
    note.update_modified(dt)

    assert note.modified == dt.timestamp()


def test_note_modified_to_datetime():
    dt = datetime.now()
    note = Note(1337, 'ham', 'spam', '', False, dt.timestamp())

    assert dt == note.modified_to_datetime()


def test_note_modified_to_str():
    dt = datetime.now()
    note = Note(1337, 'ham', 'spam', '', False, dt.timestamp())

    assert note.modified_to_str() == dt.strftime('%Y-%m-%d %H:%M:%S')


def test_note_repr():
    note = Note(1337, 'ham', 'spam', '', False, 1234)

    assert (
        repr(note) ==
        "<Note [1337]>"
    )


def test_note_str():
    dt = datetime.now()
    note = Note(1337, 'ham', 'spam', '', False, dt.timestamp())

    assert (
        str(note) ==
        f"nextcloud_notes_api.note.Note({{'id': 1337, 'content': 'ham', 'title': 'spam', 'category': '', 'favorite': False, 'modified': '{format(dt.strftime('%Y-%m-%d %H:%M:%S'))}'}})"
    )

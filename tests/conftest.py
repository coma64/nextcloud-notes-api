from random import choice, choices, randint
from string import printable
from typing import Iterator

from pytest import fixture

from nextcloud_notes_api import Note


def _random_note() -> Note:
    def random_str():
        return ''.join(choices(printable, k=randint(0, 10)))

    note_dict = {
        'title': random_str(),
        'content': random_str(),
        'category': random_str(),
        'favorite': choice([True, False]),
        'id': randint(0, 10_000),
        # https://stackoverflow.com/questions/59199985/why-is-datetimes-timestamp-method-returning-oserror-errno-22-invalid-a
        'modified': randint(90_000, 1_000_000),
    }

    # All attributes are optional
    for _ in range(randint(0, len(note_dict))):
        del note_dict[choice(list(note_dict.keys()))]

    return Note(**note_dict)


@fixture
def random_note() -> Note:
    return _random_note()


@fixture
def random_note_seq(request) -> Iterator[Note]:
    return (_random_note() for _ in range(request.param))

from typing import Iterator

from _pytest.fixtures import FixtureRequest
from pytest import fixture

from nextcloud_notes_api import Note


def _example_note() -> Note:
    return Note(
        title='Spam',
        content='Bacon',
        category='Todo',
        favorite=True,
        id=1337,
        # https://stackoverflow.com/questions/59199985/why-is-datetimes-timestamp-method-returning-oserror-errno-22-invalid-a
        modified=100_000,
    )


@fixture
def example_note() -> Note:
    """
    Returns:
        Note: Note with all attributes set
    """
    return _example_note()


@fixture
def example_note_gen(request: FixtureRequest) -> Iterator[Note]:
    """
    Args:
        request (FixtureRequest): `request.param` is the length of the generator

    Yields:
        Note: Example note, see `example_note()`
    """
    return (_example_note() for _ in range(request.param))

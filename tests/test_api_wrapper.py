from typing import ContextManager, Iterator

import pytest
from requests_mock.mocker import Mocker as RequestsMocker

from nextcloud_notes_api import (
    InsufficientNextcloudStorage,
    InvalidNextcloudCredentials,
    InvalidNoteId,
    Note,
    NoteNotFound,
    NotesApi,
)


@pytest.fixture
def notes_api():
    return NotesApi('coma64', 'pass', 'horse.agency')


@pytest.fixture
def notes_api_no_etag_caching():
    return NotesApi('coma64', 'pass', 'horse.agency', etag_caching=False)


def test_notes_api_get_api_version_requests_mock(
    notes_api: NotesApi, requests_mock: RequestsMocker
):
    requests_mock.get(
        f'https://{notes_api.hostname}/ocs/v2.php/cloud/capabilities',
        json={
            'ocs': {
                'data': {
                    'capabilities': {
                        'notes': {'api_version': ['0.2', '1.0'], 'version': '3.6.0'}
                    }
                }
            }
        },
    )

    assert '1.0' == notes_api.get_api_version()


@pytest.mark.parametrize('random_note_seq', [4, 1, 0], indirect=['random_note_seq'])
def test_notes_api_get_all_notes(
    random_note_seq: Iterator[Note],
    notes_api_no_etag_caching: NotesApi,
    requests_mock: RequestsMocker,
):
    random_note_list = list(random_note_seq)

    requests_mock.get(
        f'https://{notes_api_no_etag_caching.hostname}/index.php/apps/notes/api/v1/notes',  # noqa: E501
        json=[note.to_dict() for note in random_note_list],
    )

    notes = notes_api_no_etag_caching.get_all_notes()
    assert list(notes) == random_note_list


@pytest.mark.parametrize('random_note_seq', [4, 1, 0], indirect=['random_note_seq'])
def test_notes_api_get_all_notes_etag_cache(
    random_note_seq: Iterator[Note], notes_api: NotesApi, requests_mock: RequestsMocker
):
    random_note_list = list(random_note_seq)

    requests_mock.get(
        f'https://{notes_api.hostname}/index.php/apps/notes/api/v1/notes',
        json=[note.to_dict() for note in random_note_list],
        headers={'ETag': 'some hash'},
    )

    notes = notes_api.get_all_notes()

    assert list(notes) == random_note_list

    # This time it should return the cached notes
    with RequestsMocker() as cache_requests_mock:
        cache_requests_mock.get(
            f'https://{notes_api.hostname}/index.php/apps/notes/api/v1/notes',
            request_headers={'If-None-Match': 'some hash'},
            status_code=304,
        )
        notes = notes_api.get_all_notes()

        assert list(notes) == random_note_list


@pytest.mark.parametrize(
    'status_code, expectation', [(401, pytest.raises(InvalidNextcloudCredentials))]
)
def test_notes_api_get_all_notes_response_status_exceptions(
    status_code: int,
    expectation: ContextManager,
    notes_api: NotesApi,
    requests_mock: RequestsMocker,
):
    requests_mock.get(
        f'https://{notes_api.hostname}/index.php/apps/notes/api/v1/notes',
        status_code=status_code,
    )

    with expectation:
        notes_api.get_all_notes()


def test_notes_api_get_single_note(
    random_note: Note, notes_api: NotesApi, requests_mock: RequestsMocker
):
    requests_mock.get(
        f'https://{notes_api.hostname}/index.php/apps/notes/api/v1/notes/1337',
        json=random_note.to_dict(),
    )

    assert notes_api.get_single_note(1337) == random_note


@pytest.mark.parametrize(
    'status_code, expectation',
    [
        (400, pytest.raises(InvalidNoteId)),
        (401, pytest.raises(InvalidNextcloudCredentials)),
        (404, pytest.raises(NoteNotFound)),
    ],
)
def test_notes_api_get_single_note_response_status_exceptions(
    status_code: int,
    expectation: ContextManager,
    notes_api: NotesApi,
    requests_mock: RequestsMocker,
):
    requests_mock.get(
        f'https://{notes_api.hostname}/index.php/apps/notes/api/v1/notes/1337',
        status_code=status_code,
    )

    with expectation:
        notes_api.get_single_note(1337)


def test_notes_api_create_note(
    random_note: Note, notes_api: NotesApi, requests_mock: RequestsMocker
):
    # Server sets this
    random_note.id = None
    random_note.modified = None

    server_note = random_note
    server_note.id = 1337
    server_note.update_modified()
    requests_mock.post(
        f'https://{notes_api.hostname}/index.php/apps/notes/api/v1/notes',
        json=server_note.to_dict(),
    )

    assert notes_api.create_note(random_note) == server_note


@pytest.mark.parametrize(
    'status_code, expectation',
    [
        (401, pytest.raises(InvalidNextcloudCredentials)),
        (507, pytest.raises(InsufficientNextcloudStorage)),
    ],
)
def test_notes_api_create_note_response_status_exceptions(
    status_code: int,
    expectation: ContextManager,
    notes_api: NotesApi,
    requests_mock: RequestsMocker,
):
    requests_mock.post(
        f'https://{notes_api.hostname}/index.php/apps/notes/api/v1/notes',
        status_code=status_code,
    )

    with expectation:
        notes_api.create_note(Note())


def test_notes_api_update_note(
    random_note: Note, notes_api: NotesApi, requests_mock: RequestsMocker
):
    random_note.id = 1337

    # Server updates this
    server_note = random_note
    server_note.update_modified()

    requests_mock.put(
        f'https://{notes_api.hostname}/index.php/apps/notes/api/v1/notes/{random_note.id}',  # noqa: E501
        json=server_note.to_dict(),
    )

    assert notes_api.update_note(random_note) == server_note


def test_notes_api_update_note_id_not_set(
    random_note: Note, notes_api: NotesApi, requests_mock: RequestsMocker
):
    random_note.id = None
    # Server updates this
    server_note = random_note
    server_note.update_modified()

    requests_mock.put(
        f'https://{notes_api.hostname}/index.php/apps/notes/api/v1/notes/{random_note.id}',  # noqa: E501
        json=server_note.to_dict(),
    )

    with pytest.raises(ValueError):
        assert notes_api.update_note(random_note) == server_note


@pytest.mark.parametrize(
    'status_code, expectation',
    [
        (400, pytest.raises(InvalidNoteId)),
        (401, pytest.raises(InvalidNextcloudCredentials)),
        (404, pytest.raises(NoteNotFound)),
        (507, pytest.raises(InsufficientNextcloudStorage)),
    ],
)
def test_notes_api_update_note_response_status_exceptions(
    status_code: int,
    expectation: ContextManager,
    random_note: Note,
    notes_api: NotesApi,
    requests_mock: RequestsMocker,
):
    random_note.id = 1337

    requests_mock.put(
        f'https://{notes_api.hostname}/index.php/apps/notes/api/v1/notes/{random_note.id}',  # noqa: E501
        status_code=status_code,
    )

    with expectation:
        notes_api.update_note(random_note)


def test_notes_api_delete_note(notes_api: NotesApi, requests_mock: RequestsMocker):
    requests_mock.delete(
        f'https://{notes_api.hostname}/index.php/apps/notes/api/v1/notes/1337'
    )

    notes_api.delete_note(1337)


@pytest.mark.parametrize(
    'status_code, expectation',
    [
        (400, pytest.raises(InvalidNoteId)),
        (401, pytest.raises(InvalidNextcloudCredentials)),
        (404, pytest.raises(NoteNotFound)),
    ],
)
def test_notes_api_delete_note_response_status_exceptions(
    status_code: int,
    expectation: ContextManager,
    notes_api: NotesApi,
    requests_mock: RequestsMocker,
):
    requests_mock.delete(
        f'https://{notes_api.hostname}/index.php/apps/notes/api/v1/notes/1337',
        status_code=status_code,
    )

    with expectation:
        notes_api.delete_note(1337)


def test_notes_api_repr():
    api = NotesApi('coma64', 'pass', 'horse.agency')

    assert repr(api) == '<NotesApi [horse.agency]>'

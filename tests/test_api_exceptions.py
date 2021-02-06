from nextcloud_notes_api.api_exceptions import NotesApiError


def test_notes_api_error_str():
    notes_api_error = NotesApiError('Short message: ', username='coma64')
    assert 'Short message: username="coma64"' == str(notes_api_error)

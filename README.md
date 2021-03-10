# nextcloud-notes-api

[![Test](https://github.com/coma64/nextcloud-notes-api/workflows/Test/badge.svg)](https://github.com/coma64/nextcloud-notes-api/actions?query=workflow%3ATest)
[![Super-Linter](https://github.com/coma64/nextcloud-notes-api/workflows/Super-Linter/badge.svg)](https://github.com/coma64/nextcloud-notes-api/actions?query=workflow%3ASuper-Linter)
[![Coverage](https://img.shields.io/codecov/c/github/coma64/nextcloud-notes-api?color=%2334D058)](https://codecov.io/gh/coma64/nextcloud-notes-api)
[![PyPi](https://img.shields.io/pypi/v/nextcloud-notes-api)](https://pypi.org/project/nextcloud-notes-api/)

A [Nextcloud Notes app](https://github.com/nextcloud/notes) API wrapper.

```py
from nextcloud_notes_api import NotesApi, Note

api = NotesApi('username', 'password', 'example.org')

note = Note('Shopping List', 'Spam', favorite=True)
api.create_note(note)
```

_*nextcloud-notes-api is not supported nor endorsed by Nextcloud.*_

## Installation

```sh
pip install nextcloud-notes-api
```

## Documentation

The docs are available on [Github Pages](https://coma64.github.io/nextcloud-notes-api/).

## Contributing

Pull requests are welcome. For major changes,
please open an issue first to discuss what you would like to change.

Please make sure to update tests and documentation as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Todo

- Lazy note list with fuzzy searching through all notes
- Maintain reference to api inside note object to be able to sync, delete, ...
  through it

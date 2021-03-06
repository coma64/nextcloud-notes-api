# nextcloud-notes-api

<div style="display: flex; justify-content: space-evenly; flex-wrap: wrap;">
<a
  href="https://github.com/coma64/nextcloud-notes-api/actions?query=workflow%3ATest"
  target="_blank" style="display: inline-block; margin: 0px 0.5rem;">
<img src="https://github.com/coma64/nextcloud-notes-api/workflows/Test/badge.svg"
  alt="Test">
</a>

<a
  href="https://github.com/coma64/nextcloud-notes-api/actions?query=workflow%3ASuper-Linter"
  target="_blank" style="display: inline-block; margin: 0px 0.5rem;">
<img src="https://github.com/coma64/nextcloud-notes-api/workflows/Super-Linter/badge.svg"
  alt="Test">
</a>

<a href="https://codecov.io/gh/coma64/nextcloud-notes-api" target="_blank"
  style="display: inline-block; margin: 0px 0.5rem;">
<img
  src="https://img.shields.io/codecov/c/github/coma64/nextcloud-notes-api?color=%2334D058"
  alt="Coverage">
</a>

</div>

A [Nextcloud Notes App](https://github.com/nextcloud/notes) API wrapper

```py
from nextcloud_notes_api import NotesApi, Note

api = NotesApi('username', 'pass', 'hostname')

note = Note('Shopping List', 'Spam', favorite=True)
api.create_note(note)
```

_*nextcloud-notes-api is not supported nor endorsed by Nextcloud*_

## Installation

```sh
pip install nextcloud-notes-api
```

## Documentation

The docs are available on [Github Pages](https://coma64.github.io/nextcloud-notes-api/)

## Contributing

Pull requests are welcome. For major changes,
please open an issue first to discuss what you would like to change.

Please make sure to update tests and documentation as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

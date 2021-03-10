# Usage Examples

All interaction with the API is done through the `NotesApi` object.

## Logging In

Wrong credentials or hostname won't throw, until you interact with the API.
Any of the above can be updated, by setting the respective attribute (e.g. `NotesApi.password`).
If your host does not support ETag caching, you can disable it by passing `etag_caching=False`.

```py
from nextcloud_notes_api import NotesApi, Note

api = NotesApi('username', 'password', 'example.org')
api.password = 's3creTpaSSw0rd'
```

## Fetching Notes

Notes can be retrieved via `NotesApi.get_single_note()` by their ID.

```py
note = api.get_single_note(666)
```

To fetch all notes, use `NotesApi.get_all_notes()`.
Since `NotesApi.get_all_notes()` may return either a `typing.Iterator` or
a `collections.abc.Sequence`, it is advisibale to only iterate over it with a `for`
loop or converting it to a `list`.

```py
notes = api.get_all_notes()

for note in notes:
    print(note.title)
```

## Creating Notes

To create a new note first instanciate a `Note` and then pass it to `NotesApi.create_note()`.
`NotesApi.create_note()` returns the note with attributes set according the
its docs.

```py
# Yes, markdown is supported by the Nextcloud Notes app.
content = """# Todo
- buy chips
- buy beer
- clean up the mess from last weekend
"""
note = Note('Todo', content)
note = api.create_note(note)
```

## Updating Notes

Notes can be updated by passing a `Note` with the correct
`Note.id` to `NotesApi.update_note()`.

```py
note = api.get_single_note(1337)

note.content = 'elite'
note.update_modified()

api.update_note(note)
```

## Deleting Notes

To delete a note pass it's ID to `NotesApi.delete_note()`.

```py
api.delete_note(420)
```

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional


class Note:
    """Represents a Nextcloud Notes app note."""

    def __init__(
        self,
        title: Optional[str] = None,
        content: Optional[str] = None,
        *,
        category: Optional[str] = None,
        favorite: Optional[bool] = None,
        id: Optional[int] = None,
        modified: Optional[int] = None,
        modified_datetime: Optional[datetime] = None,
        generate_modified: bool = False,
        **_: Optional[Any],
    ):
        """See `Note.to_dict` for conversion to a `dict`.

        Args:
            title (str, optional): Note title. Defaults to None.
            content (str, optional): Note content. Defaults to None.
            category (str, optional): Note category. Defaults to None.
            favorite (bool, optional): Whether the note is marked as a favorite.
                Defaults to None.
            id (int, optional): A unique note ID. Defaults to None.
            modified (int, optional): When the note has last been modified, as int posix
                timestamp. Defaults to None.
            modified_datetime (datetime, optional): When the note has last been
                modified as datetime object, preferred over `modified`. Defaults to
                None.
            generate_modified (bool): Whether `Note.modified` should be set
                to the current time. Overrides both `modified` and `modified_datetime`.
                Defaults to False.
            _(Any, optional): Discard unused keyword arguments.
        """
        self.title = title
        """`str`: Note title."""
        self.content = content
        """`str`: Note content."""
        self.category = category
        """`str`: Note category."""
        self.favorite = favorite
        """`bool`: Whether the note is marked as a favorite."""
        self.id = id
        """`int`: A unique note id."""
        self.modified = (
            datetime.fromtimestamp(modified)
            if not modified_datetime and modified
            else modified_datetime
        )
        """`datetime.datetime`: When the note has last been modified."""

        if generate_modified:
            self.update_modified()

    def to_dict(self) -> Dict[str, Any]:
        """Generate a `dict` from this class.

        `Note.modified` is converted to a int posix timestamp.

        Returns:
            Dict[str, Any]: A `dict` containing the attributes of this class.
        """
        return {
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'favorite': self.favorite,
            'id': self.id,
            'modified': self.modified.timestamp() if self.modified else None,
        }

    def update_modified(self, dt: datetime = None) -> None:
        """Set `Note.modified` to `dt`.

        Args:
            dt (datetime): The `datetime` object to set `Note.modified` to. Defaults to
                `datetime.now()`.
        """
        if dt:
            self.modified = dt
        else:
            self.modified = datetime.now()

    def __eq__(self, other: Note) -> bool:
        return self.to_dict() == other.to_dict()

    def __repr__(self) -> str:
        return f'<Note [{self.id}]>'

    def __str__(self) -> str:
        elements = self.to_dict()
        if self.modified:
            elements['modified'] = str(self.modified)
        return f'Note[{elements}]'

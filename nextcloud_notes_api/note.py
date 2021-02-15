from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional


class Note:
    """Represents a Nextcloud Notes note"""

    def __init__(
        self,
        title: Optional[str] = '',
        content: Optional[str] = '',
        *,
        category: Optional[str] = '',
        favorite: Optional[bool] = False,
        id: Optional[int] = None,
        modified: Optional[int] = None,
        modified_datetime: Optional[datetime] = None,
        generate_modified: Optional[bool] = False,
        **_: Optional[Any],
    ):
        """See `Note.to_dict` for conversion to a dict

        Args:
            title (str, optional): Note title. Defaults to ''
            content (str, optional): Note content. Defaults to ''
            category (str, optional): Note category. Defaults to ''
            favorite (bool, optional): Whether the note is marked as a favorite.
                Defaults to False
            id (int, optional): A unique note id. Defaults to None
            modified (int, optional): When the note has last been modified as int posix
                timestamp. Defaults to None
            modified_datetime (datetime, optional): When the note has last been
                modified as datetime object, preferred over `modified`. Defaults to
                None
            generate_modified (bool, optional): Whether `Note.modified` should be set
                to the current time. Defaults to False
            _(Any, optional): Discard unused keyword arguments
        """
        self.title = title
        """str: Note title"""
        self.content = content
        """str: Note content"""
        self.category = category
        """str: Note category"""
        self.favorite = favorite
        """bool: Whether the note is marked as a favorite"""
        self.id = id
        """int: A unique note id"""
        self.modified = (
            datetime.fromtimestamp(modified)
            if not modified_datetime and modified
            else modified_datetime
        )
        """datetime: When the note has last been modified"""

        if generate_modified:
            self.update_modified()

    def to_dict(self) -> Dict[str, Any]:
        """Generate `dict` from this class

        `Note.modified` is converted to a int posix timestamp

        Returns:
            Dict[str, Any]: A `dict` containing the attributes of this class
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
        """Set `Note.modified` to `dt`

        Args:
            dt (datetime): The `datetime` object to set `Note.modified` to. Defaults to
                `datetime.now()`
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

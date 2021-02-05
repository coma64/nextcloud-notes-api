from __future__ import annotations
from typing import Dict, Any
from datetime import datetime


class Note:
    """Represents a Nextcloud Notes note"""

    def __init__(
        self,
        title: str = '',
        content: str = '',
        *,
        category: str = '',
        favorite: bool = False,
        id: int = None,
        modified: int = None,
        generate_modified: bool = False,
        **_: Any,
    ):
        """See `Note.to_dict` for conversion to a dict

        Args:
            title (str, optional): Note title. Defaults to ''
            content (str, optional): Note content. Defaults to ''
            category (str, optional): Note category. Defaults to ''
            favorite (bool, optional): Whether the note is marked as a favorite. Defaults to False
            id (int, optional): A unique note id. Defaults to None
            modified (int, optional): When the note has last been modified. Defaults to None.
            generate_modified (bool, optional): Whether`Note.modified` should be set to the
                current time. Defaults to False.
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
        self.modified = modified
        """int: When the note has last been modified"""

        if generate_modified:
            self.update_modified()

    def to_dict(self) -> Dict[str, Any]:
        """Generate `dict` from this class

        Returns:
            Dict[str, Any]: A `dict` containing the attributes of this class
        """
        return {
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'favorite': self.favorite,
            'id': self.id,
            'modified': self.modified,
        }

    def modified_to_datetime(self) -> datetime:
        """Convert the unix timestamp `Note.modified` to a `datetime` object

        Returns:
            datetime: A `datetime` object representing `Note.modified`
        """
        return datetime.fromtimestamp(self.modified)

    def modified_to_str(self, format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """Convert the unix timestamp `Note.modified` to a `str` with format `format`

        Args:
            format (str): The format string supplied to `datetime.strftime()`. Defaults to
                '%Y-%m-%d %H:%M:%S'

        Returns:
            str: A `str` representing `Note.modified`
        """
        return datetime.fromtimestamp(self.modified).strftime(format)

    def update_modified(self, dt: datetime = None) -> None:
        """Set `Note.modified` to `dt`

        Args:
            dt (datetime): The `datetime` object to set `Note.modified` to. Defaults to
                `datetime.now()`
        """
        if dt:
            self.modified = dt.timestamp()
        else:
            self.modified = datetime.now().timestamp()

    def __eq__(self, other: Note) -> bool:
        return self.to_dict() == other.to_dict()

    def __repr__(self) -> str:
        return f'<Note [{self.id}]>'

    def __str__(self) -> str:
        elements = self.to_dict()
        if self.modified:
            elements['modified'] = self.modified_to_str()
        return f'Note[{elements}]'

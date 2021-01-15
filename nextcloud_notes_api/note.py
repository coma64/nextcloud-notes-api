from __future__ import annotations
from typing import Dict, Any
from datetime import datetime


class Note:
    """Represents a Nextcloud Notes note"""

    def __init__(
        self,
        id: int,
        content: str,
        title: str,
        category: str,
        favorite: bool,
        modified: int = None,
        *,
        generate_modified: bool = False
    ):
        """See `Note.from_dict` and `Note.to_dict` for conversion from and to a dict

        Args:
            id (int): A unique note id
            content (str): Note content
            title (str): Note title
            category (str): Note category
            favorite (bool): Whether the note is marked as a favorite
            modified (int, optional): When the note has last been modified. Defaults to None.
            generate_modified (bool, optional): Whether`Note.modified` should be set to the 
                current time. Defaults to False.

        Raises:
            ValueError: Neither `modified` has been passed nor was `generate_modified` True,
                `Note.modified` cannot be left empty
        """
        if not modified and not generate_modified:
            raise ValueError(
                f'Either modified has to be passed or generate_modified has to be True.'
            )
        self.id = id
        """int: A unique note id"""
        self.content = content
        """str: Note content"""
        self.title = title
        """str: Note title"""
        self.category = category
        """str: Note category"""
        self.favorite = favorite
        """bool: Whether the note is marked as a favorite"""
        self.modified = modified
        """int: When the note has last been modified"""

        if generate_modified:
            self.update_modified(datetime.now())

    @classmethod
    def from_dict(cls: Note, data: Dict[str, Any], *, generate_modified: bool = False) -> Note:
        """Init class from a `dict` discarding unused elements

        See `Note.__init__()` args for the required values of `data`

        Args:
            data (Dict[str, Any]): The `dict` to initialize this class from
            generate_modified (bool, optional): Whether `Note.modified` should be set to the 
                current time. Defaults to False.

        Returns:
            Note: Initialized `Note`

        Raises:
            KeyError: `data` didn't contain all necessary keys
        """
        instance = cls(
            data['id'],
            data['content'],
            data['title'],
            data['category'],
            data['favorite'],
            data['modified'] if not generate_modified else None,
            generate_modified=generate_modified
        )

        return instance

    def to_dict(
        self,
        *,
        omit_modified: bool = False,
        update_modified: bool = False
    ) -> Dict[str, Any]:
        """Generate `dict` from this class

        The Nextcloud Notes api will automatically set the modified timestamp if it's missing

        Args:
            omit_modified (bool, optional): Whether to omit the `Note.modified`. Defaults to False
            update_modified (bool, optional): Whether to set `Note.modified` to the current
                time, before creating the `dict`. Defaults to False

        Returns:
            Dict[str, Any]: A `dict` containing the attributes of this class
        """
        if update_modified:
            self.update_modified(datetime.now())

        if omit_modified:
            return {
                'id': self.id,
                'content': self.content,
                'title': self.title,
                'category': self.category,
                'favorite': self.favorite,
            }
        else:
            return {
                'id': self.id,
                'content': self.content,
                'title': self.title,
                'category': self.category,
                'favorite': self.favorite,
                'modified': self.modified
            }

    def modified_to_datetime(self) -> datetime:
        """Convert the unix timestamp `Note.modified` to a `datetime` object

        Returns:
            datetime: A `datetime` object representing `Note.modified`
        """
        return datetime.fromtimestamp(self.modified)

    def modified_to_str(self) -> str:
        """Convert the unix timestamp `Note.modified` to a `str`

        Returns:
            str: A `str` representing `Note.modified`
        """
        return datetime.fromtimestamp(self.modified).strftime('%Y-%m-%d %H:%M:%S')

    def update_modified(self, dt: datetime) -> None:
        """Set `Note.modified` to `dt`

        Args:
            dt (datetime): The `datetime` object to set `Note.modified` to
        """
        self.modified = dt.timestamp()

    def __eq__(self, other: Note) -> bool:
        return self.to_dict() == other.to_dict()

    def __repr__(self) -> str:
        cls = self.__class__
        return f'{cls.__module__}.{cls.__name__}({self.to_dict()})'

    def __str__(self) -> str:
        cls = self.__class__
        elements = self.to_dict()
        elements['modified'] = self.modified_to_str()
        return f'{cls.__module__}.{cls.__name__}({elements})'

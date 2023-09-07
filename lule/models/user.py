from __future__ import annotations

from uuid import UUID

import attr
from attr.validators import instance_of

from ..constants import UserRole
from ..database.controller.user import load_user_by_email
from ..database.models import user
from ..exceptions import UserNotFound
from .course import Course


@attr.s
class User:
    id: UUID = attr.ib(validator=instance_of(UUID))
    name: str = attr.ib(validator=instance_of(str))
    email: str = attr.ib(validator=instance_of(str))
    role: UserRole = attr.ib(validator=instance_of(UserRole))
    courses: list[Course] = attr.ib(validator=instance_of(list))

    @classmethod
    async def load_from_database(cls: type[User], email: str) -> User:
        """Load user from the database.

        Args:
            email (str): user email

        Returns:
            User: user info
        """
        if not (record := await load_user_by_email(email)):
            raise UserNotFound(email=email)

        return cls.from_database_record(record)

    @classmethod
    def from_database_record(cls: type[User], record: user.User) -> User:
        """Load user from database record.

        Args:
            record (user.User): database record

        Returns:
            User: user info
        """
        return cls(
            id=record.id,
            name=record.name,
            email=record.email,
            role=UserRole(record.role),
            courses=[
                Course.from_database_record(course)
                for course in record.courses
            ],
        )

    def asdict(self) -> dict:
        """Dump User to dict."""
        return attr.asdict(self)

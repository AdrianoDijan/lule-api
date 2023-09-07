from __future__ import annotations

from uuid import UUID

import attr
from attr.validators import instance_of, optional

from ..database.controller.course import load_course
from ..database.models import course
from ..exceptions import CourseNotFound
from .document import DocumentGroup


@attr.s
class Lesson:
    id: UUID = attr.ib(validator=instance_of(UUID))
    number: int = attr.ib(validator=instance_of(int))
    name: str = attr.ib(validator=instance_of(str))
    description: str = attr.ib(validator=instance_of(str))

    @classmethod
    def from_database_record(
        cls: type[Lesson], record: course.Lesson
    ) -> Lesson:
        """Load lesson from the database record.

        :param Lesson record: database record

        :return: Lesson
        """
        return cls(
            id=record.id,
            number=record.number,
            name=record.name,
            description=record.description,
        )


@attr.s
class Course:
    id: UUID = attr.ib(validator=instance_of(UUID))
    name: str = attr.ib(validator=instance_of(str))
    icon_url: str = attr.ib(validator=instance_of(str))
    banner_url: str = attr.ib(validator=instance_of(str))
    lessons: list = attr.ib(validator=instance_of(list))
    document_groups: list[DocumentGroup] = attr.ib(
        factory=list, validator=optional(instance_of(list))
    )

    @classmethod
    async def load_from_database(cls: type[Course], id: UUID) -> Course:
        """Load course from the database.

        :param UUID id: course identifier

        :return: Course
        """
        if not (record := await load_course(id=id)):
            raise CourseNotFound(course_id=id)

        return cls.from_database_record(record)

    @classmethod
    def from_database_record(
        cls: type[Course], record: course.Course
    ) -> Course:
        """Load course from the database record.

        :param Course record: database record

        :return: Course
        """
        return cls(
            id=record.id,
            name=record.name,
            icon_url=record.icon_url,
            banner_url=record.banner_url,
            lessons=[
                Lesson.from_database_record(lesson)
                for lesson in record.lessons or []
            ],
            document_groups=DocumentGroup.from_database_records(
                record.documents or []
            ),
        )

    def asdict(self) -> dict:
        """Dump Course to dict."""
        return {
            key: value
            for key, value in attr.asdict(self).items()
            if value is not None
        } | {
            "document_groups": [
                document_group.asdict()
                for document_group in self.document_groups
            ]
        }

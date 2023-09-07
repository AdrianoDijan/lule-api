from uuid import UUID

from pydantic import BaseModel, HttpUrl

from .document import DocumentGroup


class Lesson(BaseModel):
    id: UUID
    number: int
    name: str
    description: str


class CourseInfo(BaseModel):
    id: UUID
    name: str
    icon_url: HttpUrl


class Course(CourseInfo):
    banner_url: HttpUrl
    lessons: list[Lesson]
    document_groups: list[DocumentGroup]


class Courses(BaseModel):
    courses: list[Course]

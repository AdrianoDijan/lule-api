from __future__ import annotations

from uuid import UUID

from ..models.course import Course, Lesson
from ..models.document import Document


async def load_course(id: UUID) -> Course | None:
    """Load course from the database.

    :param UUID id: course identifier

    :return: Course
    """
    result = (
        await Course.outerjoin(Lesson, Lesson.course_id == Course.id)
        .outerjoin(Document, Document.course_id == Course.id)
        .select()
        .where(Course.id == id)
        .gino.load(
            Course.distinct(Course.id).load(
                add_lesson=Lesson.distinct(Lesson.id).load(),
                add_document=Document.distinct(Document.id).load(),
            )
        )
        .all()
    )

    return result[0] if result else 0

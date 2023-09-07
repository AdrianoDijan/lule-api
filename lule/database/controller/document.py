from __future__ import annotations

from uuid import UUID

from sqlalchemy import and_, or_

from ..models.course import Course, Lesson
from ..models.document import Document


async def get_document(course_id: UUID, document_id: UUID) -> Document | None:
    """Load document from the database.

    Args:
        course_id (UUID): course identifier
        document_id (UUID): document identifier

    Returns:
        Document: document info if found, None otherwise
    """
    return await Document.query.where(
        and_(Document.course_id == course_id, Document.id == document_id)
    ).gino.first()


async def update_document(
    document_id: UUID, document: dict
) -> Document | None:
    """Update existing document.

    Args:
        document_id (UUID): document identifier
        document (dict): document info

    Return:
        Document | None: Document if updated, None otherwise
    """
    record = await Document.get(document_id)
    if not record:
        return None

    return await record.update(**document).apply()


async def store_document(document: dict) -> Document:
    """Store document to the database.

    Args:
        document (dict): document info

    Returns:
        Document
    """
    return await Document.create(**document)


async def search_documents_by_query_string(query: str) -> list[Course]:
    """Search document by query string.

    Args:
        query (str): query string

    Returns:
        list[Course]
    """
    return (
        await Course.outerjoin(Lesson, Lesson.course_id == Course.id)
        .join(Document, Document.course_id == Course.id)
        .select()
        .where(
            or_(
                Document.name.contains(query),
                Document.filename.contains(query),
            )
        )
        .gino.load(
            Course.distinct(Course.id).load(
                add_lesson=Lesson.distinct(Lesson.id),
                add_document=Document.distinct(Document.id),
            )
        )
        .all()
    )

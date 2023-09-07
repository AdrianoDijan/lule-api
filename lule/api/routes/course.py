from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from ...constants import ActionStatus
from ...models import course, document
from ..schemas.common import StatusResponse
from ..schemas.course import Course
from ..schemas.document import DocumentInfo, DocumentRequest, DocumentUpdate

router = APIRouter()


@router.get("/courses/{course_id}", tags=["Courses"], response_model=Course)
async def get_course(course_id: UUID) -> Course:
    """Get course by id."""
    course_info = await course.Course.load_from_database(id=course_id)
    data = course_info.asdict()
    return data


@router.get(
    "/courses/{course_id}/documents/{document_id}",
    tags=["Courses"],
    status_code=307,
)
async def get_document(course_id: UUID, document_id: UUID) -> RedirectResponse:
    """Get document."""
    document_info = await document.Document.load_from_database(
        course_id=course_id, document_id=document_id
    )
    redirect_url = await document_info.get_signed_url()
    return RedirectResponse(url=redirect_url)


@router.patch(
    "/courses/{course_id}/documents/{document_id}",
    tags=["Courses"],
    response_model=DocumentInfo,
)
async def update_document(
    course_id: UUID, document_id: UUID, update: DocumentUpdate
):
    document_info = await document.Document.load_from_database(
        course_id=course_id, document_id=document_id
    )
    await document_info.update(update.dict(exclude_unset=True))

    return document_info.asdict()


@router.post(
    "/courses/{course_id}/documents",
    tags=["Courses"],
    response_model=StatusResponse,
)
async def create_document(
    course_id: UUID, body: DocumentRequest
) -> StatusResponse:
    """Create new document."""
    new_document = document.Document.from_api_request(
        course_id=course_id, body=body.dict()
    )

    await new_document.upload()
    await new_document.store()

    return {"status": ActionStatus.SUCCESS}

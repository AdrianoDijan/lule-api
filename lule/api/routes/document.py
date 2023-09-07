from fastapi import APIRouter

from ...database.controller.document import search_documents_by_query_string
from ...models import course
from ..schemas.course import Courses

router = APIRouter()


@router.get("/documents", response_model=Courses)
async def search_documents(query: str):
    search_results = await search_documents_by_query_string(query=query)
    courses = [
        course.Course.from_database_record(result) for result in search_results
    ]

    return {"courses": [course_info.asdict() for course_info in courses]}

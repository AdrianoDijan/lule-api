from typing import Optional

from ..models.course import Course, CourseUser, Lesson
from ..models.user import User


async def load_user_by_email(email: str) -> Optional[User]:
    """Load user by email.

    Args:
        email (str): user email

    Returns:
        Optional[User]: User object if found, None otherwise
    """
    result = (
        await User.outerjoin(CourseUser, User.id == CourseUser.user_id)
        .outerjoin(Course, CourseUser.course_id == Course.id)
        .outerjoin(Lesson, Course.id == Lesson.course_id)
        .select()
        .where(User.email == email)
        .gino.load(
            User.distinct(User.id).load(
                add_course=Course.distinct(Course.id).load(
                    add_lesson=Lesson.distinct(Lesson.id)
                )
            )
        )
        .all()
    )

    return result[0] if result else None

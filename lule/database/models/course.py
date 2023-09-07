from sqlalchemy.dialects.postgresql import UUID

from .base import db


class Lesson(db.Model):
    __tablename__ = "lesson"
    id = db.Column(UUID, primary_key=True)
    course_id = db.Column(
        UUID, db.ForeignKey("course.id"), index=True, nullable=False
    )
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.VARCHAR(80), nullable=False)
    description = db.Column(db.String(), nullable=False)


class CourseUser(db.Model):
    __tablename__ = "course_user"

    id = db.Column(UUID, primary_key=True)
    course_id = db.Column(
        UUID, db.ForeignKey("course.id"), index=True, nullable=False
    )
    user_id = db.Column(
        UUID, db.ForeignKey("user.id"), index=True, nullable=False
    )

    _uniq_constr = db.UniqueConstraint(
        "course_id", "user_id", name="course_uc"
    )


class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(UUID, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    icon_url = db.Column(db.String(), nullable=False)
    banner_url = db.Column(db.String(), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._lessons = []
        self._documents = []

    @property
    def lessons(self):
        return self._lessons

    @lessons.setter  # type: ignore
    def add_lesson(self, lesson: Lesson):
        if lesson not in self._lessons:
            self._lessons.append(lesson)

    @property
    def documents(self):
        return self._documents

    @documents.setter  # type: ignore
    def add_document(self, document):
        if document not in self._documents:
            self._documents.append(document)

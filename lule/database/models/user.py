from sqlalchemy.dialects.postgresql import UUID

from .base import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(UUID, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=True, unique=True)
    role = db.Column(db.String())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._courses = []

    @property
    def courses(self):
        return self._courses

    @courses.setter  # type: ignore
    def add_course(self, course):
        if course not in self._courses:
            self._courses.append(course)

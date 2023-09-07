from sqlalchemy.dialects.postgresql import UUID

from .base import db


class Document(db.Model):
    __tablename__ = "document"

    id = db.Column(UUID, primary_key=True)
    group_name = db.Column(db.VARCHAR(80), nullable=False)
    course_id = db.Column(
        UUID, db.ForeignKey("course.id"), index=True, nullable=False
    )
    name = db.Column(db.String(), nullable=False)
    file_url = db.Column(db.String(), nullable=False)
    filename = db.Column(db.String(), nullable=False)
    content_type = db.Column(db.VARCHAR(260), nullable=False)
    status = db.Column(db.VARCHAR(80), nullable=False)

"""Initial migration

Revision ID: 4525c1d65466
Revises:
Create Date: 2023-09-07 10:56:08.833460

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "4525c1d65466"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "course",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("icon_url", sa.String(), nullable=False),
        sa.Column("banner_url", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("role", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "course_user",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("course_id", postgresql.UUID(), nullable=False),
        sa.Column("user_id", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("course_id", "user_id", name="course_uc"),
    )
    op.create_index(
        op.f("ix_course_user_course_id"),
        "course_user",
        ["course_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_course_user_user_id"),
        "course_user",
        ["user_id"],
        unique=False,
    )
    op.create_table(
        "document",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("group_name", sa.VARCHAR(length=80), nullable=False),
        sa.Column("course_id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("file_url", sa.String(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("content_type", sa.VARCHAR(length=260), nullable=False),
        sa.Column("status", sa.VARCHAR(length=80), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_document_course_id"), "document", ["course_id"], unique=False
    )
    op.create_table(
        "lesson",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("course_id", postgresql.UUID(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=80), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_lesson_course_id"), "lesson", ["course_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_lesson_course_id"), table_name="lesson")
    op.drop_table("lesson")
    op.drop_index(op.f("ix_document_course_id"), table_name="document")
    op.drop_table("document")
    op.drop_index(op.f("ix_course_user_user_id"), table_name="course_user")
    op.drop_index(op.f("ix_course_user_course_id"), table_name="course_user")
    op.drop_table("course_user")
    op.drop_table("user")
    op.drop_table("course")
    # ### end Alembic commands ###
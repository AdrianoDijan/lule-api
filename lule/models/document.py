from __future__ import annotations

from typing import DefaultDict
from uuid import UUID, uuid4

import attr
from attr.validators import instance_of, optional
from datauri import DataURI

from ..constants import DocumentStatus
from ..database.controller.document import (
    get_document,
    store_document,
    update_document,
)
from ..database.models import document
from ..exceptions import DocumentNotFound
from ..settings import API_HOST, BUCKET_NAME
from ..storage.s3 import S3Client


@attr.s
class Document:
    id: UUID = attr.ib(validator=instance_of(UUID))
    group_name: str = attr.ib(validator=instance_of(str))
    course_id: UUID = attr.ib(validator=instance_of(UUID))
    name: str = attr.ib(validator=instance_of(str))
    filename: str = attr.ib(validator=instance_of(str))
    content_type: str = attr.ib(validator=instance_of(str))
    status: DocumentStatus = attr.ib(validator=instance_of(DocumentStatus))

    content: DataURI | None = attr.ib(
        default=None, validator=optional(instance_of(DataURI))
    )
    file_url: str | None = attr.ib(
        default=None, validator=optional(instance_of(str))
    )

    @classmethod
    def from_api_request(
        cls: type[Document], course_id: UUID, body: dict
    ) -> Document:
        """Create document object from the api request.

        Args:
            course_id (UUID): course identifier
            body (dict): request body

        Returns:
            Document
        """
        content: DataURI = body["content"]
        return cls(
            id=uuid4(),
            course_id=course_id,
            group_name=body["group_name"],
            name=body["name"],
            filename=body["filename"],
            content_type=content.mimetype,
            status=DocumentStatus.PENDING,
            content=content,
        )

    @classmethod
    async def load_from_database(
        cls: type[Document], course_id: UUID, document_id: UUID
    ) -> Document:
        """Load document from the database.

        Args:
            course_id (UUID): course identifier
            document_id (UUID): document identifier

        Returns:
            Document: document info
        """
        if not (
            record := await get_document(
                course_id=course_id, document_id=document_id
            )
        ):
            raise DocumentNotFound(
                course_id=course_id, document_id=document_id
            )

        return cls.from_database_record(record=record)

    @classmethod
    def from_database_record(
        cls: type[Document], record: document.Document
    ) -> Document:
        """Load document from the database record.

        :param Document record: database record

        :return: Document
        """
        return cls(
            id=record.id,
            group_name=record.group_name,
            course_id=record.course_id,
            name=record.name,
            filename=record.filename,
            file_url=record.file_url,
            content_type=record.content_type,
            status=DocumentStatus(record.status),
        )

    async def get_signed_url(self) -> str:
        """Get signed URL for a file."""
        if not self.file_url.startswith("s3://"):
            return self.file_url

        key = self.file_url.lstrip("s3://").split("/", maxsplit=1)[-1]
        return await S3Client.generate_signed_url(object_key=key)

    async def update(self, update: dict) -> None:
        """Update existing document.

        Args:
            update (dict): updated info

        Returns:
            None
        """
        self.name = update.get("name", self.name)
        self.status = update.get("status", self.status)

        await update_document(
            document_id=self.id,
            document={"name": self.name, "status": self.status},
        )

        return None

    async def upload(self) -> None:
        """Upload file to the S3 storage."""
        object_key = (
            f"courses/{self.course_id}/documents/{self.id}_{self.filename}"
        )
        await S3Client.upload(content=self.content.data, object_key=object_key)
        self.file_url = f"s3://{BUCKET_NAME}/{object_key}"

    async def store(self) -> None:
        """Store document to the database."""
        await store_document(
            {
                "id": self.id,
                "group_name": self.group_name,
                "course_id": self.course_id,
                "name": self.name,
                "filename": self.filename,
                "file_url": self.file_url,
                "content_type": self.content_type,
                "status": self.status,
            }
        )

    @property
    def public_url(self) -> str:
        """Generate public url to access the file."""
        return f"{API_HOST.rstrip('/')}/courses/{self.course_id}/documents/{self.id}"

    def asdict(self) -> dict:
        """Dump Document to dict."""
        data = attr.asdict(self)
        data["file_url"] = self.public_url
        return data


@attr.s
class DocumentGroup:
    name: str = attr.ib(validator=instance_of(str))
    documents: list[Document] = attr.ib(validator=instance_of(list))

    @classmethod
    def from_database_records(
        cls: type[DocumentGroup], records: list[document.Document]
    ) -> list[DocumentGroup]:
        """Load document groups from the database record.

        :param list records: list of database records

        :return: list[DocumentGroup]
        """
        groups = DefaultDict(lambda: [])
        for record in records:
            groups[record.group_name].append(record)

        return [
            cls(
                name=group_name,
                documents=[
                    Document.from_database_record(record)
                    for record in document_records
                ],
            )
            for group_name, document_records in groups.items()
        ]

    def asdict(self) -> dict:
        """Dump DocumentGroup to dict."""
        return {
            "name": self.name,
            "documents": [
                document_info.asdict() for document_info in self.documents
            ],
        }

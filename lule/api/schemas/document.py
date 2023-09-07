from __future__ import annotations

from uuid import UUID

from datauri import DataURI
from pydantic import AnyHttpUrl, BaseModel, Field

from ...constants import DocumentStatus


class DocumentInfo(BaseModel):
    id: UUID
    name: str
    filename: str = Field(examples=["document.pdf"])
    file_url: AnyHttpUrl
    content_type: str = Field(examples=["application/pdf"])
    status: DocumentStatus


class DocumentUpdate(BaseModel):
    name: str | None
    status: DocumentStatus


class DocumentRequest(BaseModel):
    name: str
    filename: str = Field(examples=["document.pdf"])
    group_name: str = Field(examples=["Predavanja"])
    content: DataURI


class DocumentGroup(BaseModel):
    name: str = Field(examples=["Predavanja"])
    documents: list[DocumentInfo]

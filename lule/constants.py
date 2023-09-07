import enum


@enum.unique
class UserRole(str, enum.Enum):
    ADMINISTATOR = "administrator"
    STUDENT = "student"


@enum.unique
class DocumentStatus(str, enum.Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"


@enum.unique
class ActionStatus(str, enum.Enum):
    SUCCESS = "success"
    FAILURE = "failure"

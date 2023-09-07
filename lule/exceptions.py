from uuid import UUID


class APIError(Exception):
    """Base API exception class."""

    error_code = "api_error.unexpected"
    status_code = 500
    message = None

    @property
    def error_response(self) -> dict:
        """Build error response from API error."""
        return {
            "detail": [
                {
                    "msg": self.message,
                    "type": self.error_code,
                }
            ]
        }


class NotFoundAPIError(APIError):
    """Base 'Not Found' API error class."""

    status_code = 404


class CourseNotFound(NotFoundAPIError):
    """Course with given id not found."""

    error_code = "not_found.course"

    def __init__(self, course_id: UUID):
        self.message = f"Course with id '{course_id}' could not be found."
        super().__init__(self.message)


class UserNotFound(NotFoundAPIError):
    """User with given email not found."""

    error_code = "not_found.user"

    def __init__(self, email: UUID):
        self.message = f"User with email '{email}' could not be found."
        super().__init__(self.message)


class DocumentNotFound(NotFoundAPIError):
    """User with given email not found."""

    error_code = "not_found.document"

    def __init__(self, course_id: UUID, document_id: UUID):
        self.message = (
            f"Document with id '{course_id}/{document_id}' could not be found."
        )
        super().__init__(self.message)

from fastapi import FastAPI

from ..database.models import db
from .middleware import CustomExceptionMiddleware
from .routes import course, document, user


def get_app():
    app = FastAPI(title="lule API")
    db.init_app(app)
    return app


application = get_app()

application.include_router(user.router)
application.include_router(course.router)
application.include_router(document.router)

application.add_middleware(CustomExceptionMiddleware)

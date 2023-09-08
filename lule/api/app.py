from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..database.models import db
from .middleware import CustomExceptionMiddleware
from .routes import course, document, user

ORIGINS = [
    "https://lule.adriano.sh",
    "http://localhost:3000",
    "https://lule.vercel.app",
]


def get_app():
    app = FastAPI(title="lule API")
    db.init_app(app)
    return app


application = get_app()

application.include_router(user.router)
application.include_router(course.router)
application.include_router(document.router)

application.add_middleware(CustomExceptionMiddleware)

application.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

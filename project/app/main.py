from fastapi import FastAPI

from project.app.startup_tasks import generate_db
from project.app.presentation import rest
from project.app.infrastructure import application


app: FastAPI = application.create(
    rest_routers=(rest.authentication.router, rest.posts.router, rest.analytics.router),
    startup_tasks=[generate_db],
    shutdown_tasks=[]
)

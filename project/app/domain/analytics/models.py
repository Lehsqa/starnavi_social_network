from datetime import date

from project.app.infrastructure.models import InternalModel


# Internal models
# ------------------------------------------------------
class AnalyticsLikes(InternalModel):
    date: date
    likes_count: int

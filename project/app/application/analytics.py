from datetime import date, datetime

from project.app.application.users import update_user
from project.app.domain.analytics.models import AnalyticsLikes
from project.app.domain.likes import LikesRepository


async def get_likes_analytics_data(date_from: date, date_to: date, user_id: int) -> list[AnalyticsLikes]:
    date_from = datetime.combine(date_from, datetime.min.time())
    date_to = datetime.combine(date_to, datetime.min.time())

    analytics_data = [
        item async for item in LikesRepository().count(date_from=date_from, date_to=date_to)
    ]
    await update_user(id=user_id, field='last_request', data=datetime.now())

    return analytics_data

from rq import Queue

from app.core.redis import redis_client


email_queue = Queue(
    "emails",
    connection=redis_client,
)

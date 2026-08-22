import secrets
from uuid import UUID

from app.core.redis import redis_client


VERIFICATION_TOKEN_TTL = 30 * 60  # 30 minutes


def create_verification_token(user_id: UUID) -> str:
    token = secrets.token_urlsafe(32)

    key = f"email_verification:{token}"

    redis_client.setex(
        key,
        VERIFICATION_TOKEN_TTL,
        str(user_id),
    )

    return token

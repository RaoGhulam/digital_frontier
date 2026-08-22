from enum import StrEnum


class AdminRole(StrEnum):
    MODERATOR = "moderator"
    SUPERADMIN = "superadmin"


class PostStatus(StrEnum):
    PENDING = "pending"
    PUBLISHED = "published"
    REJECTED = "rejected"


class ModerationAction(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"


class ReactionType(StrEnum):
    LIKE = "like"
    DISLIKE = "dislike"


class UserStatus(StrEnum):
    ACTIVE = "active"
    DELETED = "deleted"
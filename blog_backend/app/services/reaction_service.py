from math import ceil
from typing import Optional
from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from app.models.post import Post
from app.models.reaction import PostReaction, ReactionType

from app.schemas.post import PostListItem

from app.core.exceptions import ReactionNotFoundError
from app.core.enums import ReactionType


def get_post_reaction_counts(db: Session, post_id: int):
    reactions = (
        db.query(PostReaction.reaction)
        .filter(PostReaction.post_id == post_id)
        .all()
    )

    likes = sum(
        1 for r in reactions
        if r.reaction == ReactionType.LIKE
    )
    dislikes = sum(
        1 for r in reactions
        if r.reaction == ReactionType.DISLIKE
    )

    return {
        "likes": likes,
        "dislikes": dislikes,
    }


def get_liked_posts_by_user(
    db: Session,
    user_id,
    page: int = 1,
    per_page: int = 9,
):
    query = (
        db.query(Post)
        .join(PostReaction, Post.id == PostReaction.post_id)
        .options(joinedload(Post.author))
        .filter(
            PostReaction.user_id == user_id,
            PostReaction.reaction == ReactionType.LIKE   # ✅ FIXED
        )
        .order_by(desc(Post.created_at))
        .distinct()
    )

    total = query.count()

    posts = (
        query.offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    post_items = [
        PostListItem(
            id=post.id,
            title=post.title,
            slug=post.slug,
            category=post.category,
            author_name=post.author.username,
            published_at=post.published_at,
            created_at=post.created_at,
        )
        for post in posts
    ]

    return {
        "posts": post_items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": ceil(total / per_page),
        },
    }



def set_reaction(
    db: Session,
    post_id: UUID,
    user_id: int,
    reaction: Optional[ReactionType],  # LIKE / DISLIKE / None
):
    existing = db.query(PostReaction).filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()

    # Case 1: remove reaction
    if reaction is None:
        if not existing:
            raise ReactionNotFoundError(
                f"No reaction found for user_id={user_id}, post_id={post_id}"
            )

        db.delete(existing)
        commit_transaction(db)

        return {
            "success": True,
            "message": "Reaction removed successfully",
            "post_id": post_id,
            "reaction": None
        }

    # Case 2: update existing reaction
    if existing:
        existing.reaction = reaction
        commit_transaction(db)
        db.refresh(existing)

        return {
            "success": True,
            "message": "Reaction updated successfully",
            "post_id": post_id,
            "reaction": existing.reaction
        }

    # Case 3: create new reaction
    new_reaction = PostReaction(
        user_id=user_id,
        post_id=post_id,
        reaction=reaction
    )

    db.add(new_reaction)
    commit_transaction(db)
    db.refresh(new_reaction)

    return {
        "success": True,
        "message": "Reaction added successfully",
        "post_id": post_id,
        "reaction": new_reaction.reaction
    }


# ---------------------------
# Helper
# ---------------------------
def commit_transaction(db: Session):
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
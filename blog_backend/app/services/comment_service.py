from math import ceil
from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.comment import Comment
from app.models.post import Post

from app.schemas.post import PostListItem

from app.core.exceptions import (
    CommentNotFoundError,
    CommentPermissionError,
    PostNotFoundError,
)


def get_post_comments_tree(db: Session, post_id: UUID):
    comments = (
        db.query(Comment)
        .options(joinedload(Comment.user))
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
        .all()
    )

    comment_map = {}
    root_comments = []

    for c in comments:
        comment_map[c.id] = {
            "id": c.id,
            "post_id": c.post_id,
            "content": c.content,
            "user": {
                "id": c.user.id,
                "username": c.user.username,
            },
            "created_at": c.created_at,
            "replies": [],
        }

    for c in comments:
        node = comment_map[c.id]

        if c.parent_id:
            parent = comment_map.get(c.parent_id)

            if parent:
                parent["replies"].append(node)
        else:
            root_comments.append(node)

    return root_comments


def get_commented_posts_by_user(
    db: Session,
    user_id,
    page: int = 1,
    per_page: int = 9,
):
    query = (
        db.query(Post)
        .join(Comment, Post.id == Comment.post_id)
        .options(joinedload(Post.author))
        .filter(Comment.user_id == user_id)
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


def add_comment(
    db: Session,
    post_id: UUID,
    user_id: UUID,
    content: str,
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise PostNotFoundError(
            f"Post with id {post_id} was not found."
        )

    comment = Comment(
        post_id=post_id,
        user_id=user_id,
        content=content,
    )

    db.add(comment)
    commit_transaction(db)

    comment = (
        db.query(Comment)
        .options(
            joinedload(Comment.user),
            selectinload(Comment.replies),
        )
        .filter(Comment.id == comment.id)
        .first()
    )

    return comment


def reply_to_comment(
    db: Session,
    comment_id: UUID,
    user_id: UUID,
    content: str,
):
    parent_comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .first()
    )

    if not parent_comment:
        raise CommentNotFoundError(
            f"Comment with id {comment_id} was not found."
        )

    reply = Comment(
        post_id=parent_comment.post_id,
        user_id=user_id,
        parent_id=parent_comment.id,
        content=content,
    )

    db.add(reply)
    commit_transaction(db)
    db.refresh(reply)

    return reply


def delete_comment_by_user(
    db: Session,
    comment_id,
    user_id,
):
    comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .first()
    )

    if not comment:
        raise CommentNotFoundError(
            f"Comment with id {comment_id} was not found."
        )

    if comment.user_id != user_id:
        raise CommentPermissionError(
            f"User {user_id} is not authorized to delete comment {comment_id}."
        )

    db.delete(comment)
    commit_transaction(db)


# ---------------------------
# Helper
# ---------------------------
def commit_transaction(db: Session):
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
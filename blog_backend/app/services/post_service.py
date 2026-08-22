from math import ceil

from sqlalchemy import func, case, asc, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.models.pending_post import PendingPost
from app.models.post import Post
from app.models.user import User
from app.models.reaction import PostReaction
from app.models.comment import Comment

from app.services.comment_service import get_post_comments_tree
from app.services.reaction_service import get_post_reaction_counts

from app.core.exceptions import (
    PostNotFoundError,
    PermissionDenied,
    DuplicateSlugError,
    DatabaseError,
)

from app.core.enums import PostStatus

def get_posts(
    db: Session,
    category: str = "all",
    sort_by: str = "latest",
    page: int = 1,
    per_page: int = 9,
):
    # Count likes/dislikes per post
    reaction_counts = (
        db.query(
            PostReaction.post_id,
            func.count(
                case(
                    (PostReaction.reaction == "like", 1)
                )
            ).label("like_count"),
            func.count(
                case(
                    (PostReaction.reaction == "dislike", 1)
                )
            ).label("dislike_count"),
        )
        .group_by(PostReaction.post_id)
        .subquery()
    )

    # Count comments per post
    comment_counts = (
        db.query(
            Comment.post_id,
            func.count(Comment.id).label("comment_count")
        )
        .group_by(Comment.post_id)
        .subquery()
    )

    query = (
        db.query(
            Post,
            func.coalesce(
                reaction_counts.c.like_count,
                0
            ).label("like_count"),
            func.coalesce(
                reaction_counts.c.dislike_count,
                0
            ).label("dislike_count"),
            func.coalesce(
                comment_counts.c.comment_count,
                0
            ).label("comment_count"),
        )
        .options(joinedload(Post.author))
        .outerjoin(
            reaction_counts,
            reaction_counts.c.post_id == Post.id
        )
        .outerjoin(
            comment_counts,
            comment_counts.c.post_id == Post.id
        )
        .filter(Post.status == PostStatus.PUBLISHED)
    )

    # category filter
    if category.lower() != "all":
        query = query.filter(Post.category == category)

    # sorting
    if sort_by == "oldest":
        query = query.order_by(asc(Post.created_at))
    else:
        query = query.order_by(desc(Post.created_at))

    # total records before pagination
    total = query.count()

    posts = (
        query
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    result = []

    for (
        post,
        like_count,
        dislike_count,
        comment_count
    ) in posts:

        result.append(
            {
                "id": post.id,
                "title": post.title,
                "slug": post.slug,
                "category": post.category,
                "author_name": post.author.username,
                "published_at": post.published_at,
                "created_at": post.created_at,

                "likes": like_count,
                "dislikes": dislike_count,
                "comments": comment_count,
            }
        )

    return {
        "posts": result,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": ceil(total / per_page),
        },
    }


from sqlalchemy import and_

def get_post_detail(
    db: Session,
    slug: str,
    current_user=None,
):
    query = (
        db.query(Post, PostReaction)
        .outerjoin(
            PostReaction,
            and_(
                PostReaction.post_id == Post.id,
                PostReaction.user_id == (
                    current_user.id if current_user else None
                ),
            ),
        )
        .options(
            joinedload(Post.author)
        )
        .filter(
            Post.slug == slug,
            Post.status == PostStatus.PUBLISHED,
        )
    )

    result = query.first()

    if not result:
        raise PostNotFoundError("Post not found")

    post, user_reaction = result

    reactions = get_post_reaction_counts(db, post.id)
    comments = get_post_comments_tree(db, post.id)

    def count_comments(comments):
        return sum(
            1 + count_comments(comment["replies"])
            for comment in comments
        )

    comment_count = count_comments(comments)

    return {
        "id": post.id,
        "title": post.title,
        "slug": post.slug,
        "category": post.category,
        "content": post.content,
        "published_at": post.published_at,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "author": {
            "id": post.author.id,
            "username": post.author.username,
        },
        "comment_count": comment_count,
        "reactions": reactions,
        "user_reaction": (
            user_reaction.reaction
            if user_reaction
            else None
        ),
        "comments": comments,
    }


def create_pending_post(db: Session, user: User, data):
    if db.query(Post).filter(Post.slug == data.slug).first():
        raise DuplicateSlugError("Slug already exists in published posts")

    if db.query(PendingPost).filter(PendingPost.slug == data.slug).first():
        raise DuplicateSlugError("Slug already exists in pending posts")

    pending = PendingPost(
        author_id=user.id,
        title=data.title,
        content=data.content,
        slug=data.slug,
        category=data.category,
    )

    db.add(pending)

    try:
        commit_transaction(db)

    except IntegrityError as e:
        db.rollback()

        if "slug" in str(e.orig).lower():
            raise DuplicateSlugError("Slug already exists")

        raise DatabaseError("Database constraint error")

    return pending


def delete_post_by_slug(db: Session, slug: str, user_id):
    post = db.query(Post).filter(Post.slug == slug).first()

    if not post:
        raise PostNotFoundError("Post not found")

    if post.author_id != user_id:
        raise PermissionDenied("You are not allowed to delete this post")

    db.delete(post)
    commit_transaction(db)

    return post



def get_user_posts(
    db: Session,
    user_id,
    is_published: str = "all",
    sort_by: str = "latest",
    page: int = 1,
    per_page: int = 9,
):
    query = (
        db.query(Post)
        .options(joinedload(Post.author))
        .filter(Post.author_id == user_id)
    )

    # -------------------
    # filter by status
    # -------------------
    if is_published == "published":
        query = query.filter(Post.status == PostStatus.PUBLISHED)
    elif is_published == "unpublished":
        query = query.filter(Post.status != PostStatus.PUBLISHED)

    # -------------------
    # sorting
    # -------------------
    if sort_by == "oldest":
        query = query.order_by(asc(Post.created_at))
    else:
        query = query.order_by(desc(Post.created_at))

    total = query.count()

    posts = (
        query.offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    result = []

    for post in posts:
        result.append(
            {
                "id": post.id,
                "title": post.title,
                "slug": post.slug,
                "category": post.category,
                "author_name": post.author.username,
                "published_at": post.published_at,
                "created_at": post.created_at,
            }
        )

    return {
        "posts": result,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": ceil(total / per_page),
        },
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
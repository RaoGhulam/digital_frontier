"use client";

import { PostDetail, ReactionType } from "@/types/post";
import { reactToPost } from "@/lib/api/reactions";
import { addComment } from "@/lib/api/comments";
import CommentItem from "@/components/comment/CommentItem";
import CommentForm from "@/components/comment/CommentForm"
import { useState } from "react";
import { ThumbsUp, ThumbsDown, MessageCircle } from "lucide-react";


interface Props {
  post: PostDetail;
}

export default function PostDetails({ post }: Props) {
  const [likes, setLikes] = useState(post.reactions.likes);
  const [dislikes, setDislikes] = useState(post.reactions.dislikes);
  const [userReaction, setUserReaction] = useState<ReactionType | null>(
    post.user_reaction
  );
  const [loadingReaction, setLoadingReaction] = useState(false);
  const [loadingComment, setLoadingComment] = useState(false);
  const [comments, setComments] = useState(post.comments);
  const [commentCount, setCommentCount] = useState(post.comment_count);

  const handleReaction = async (reaction: "like" | "dislike") => {
    if (loadingReaction) return;

    const newReaction =
      userReaction === reaction.toLowerCase()
        ? null
        : reaction.toLowerCase() as ReactionType;

    const previousReaction = userReaction;

    // Optimistic UI update
    if (previousReaction === "like") {
      setLikes((prev) => prev - 1);
    }

    if (previousReaction === "dislike") {
      setDislikes((prev) => prev - 1);
    }

    if (newReaction === "like") {
      setLikes((prev) => prev + 1);
    }

    if (newReaction === "dislike") {
      setDislikes((prev) => prev + 1);
    }

    setUserReaction(newReaction);

    try {
      setLoadingReaction(true);

      await reactToPost({
        post_id: post.id,
        reaction: reaction,
      });

    } catch (err) {
      // rollback if API fails
      setUserReaction(previousReaction);

      if (previousReaction === "like") {
        setLikes((prev) => prev + 1);
      }

      if (previousReaction === "dislike") {
        setDislikes((prev) => prev + 1);
      }

      if (newReaction === "like") {
        setLikes((prev) => prev - 1);
      }

      if (newReaction === "dislike") {
        setDislikes((prev) => prev - 1);
      }

      if (err instanceof Error && err.message === "UNAUTHORIZED") {
        alert("Please log in first to react to this post.");
        return;
      }

      console.error(err);
      alert("Failed to submit your reaction. Please try again.");
    } finally {
      setLoadingReaction(false);
    }
  };

  const handleAddComment = async (text: string) => {
    if (loadingComment) return;

    try {
      setLoadingComment(true);

      const newComment = await addComment({
        post_id: post.id,
        content: text,
      });

      setComments((prev) => [
        ...prev,
        newComment,
      ]);

      setCommentCount((prev) => prev + 1);

    } catch (err) {
      if (err instanceof Error && err.message === "UNAUTHORIZED") {
        alert("Please log in first to comment.");
        return;
      }

      console.error(err);
      alert("Failed to add comment. Please try again.");
    } finally {
      setLoadingComment(false);
    }
  };

  return (
    <article className="mx-auto max-w-4xl">

      {/* Article Card */}
      <div
        className="
          rounded-lg
          border
          border-[#E4E4E0]
          bg-[#FAFAF8]
          p-8
          md:p-12
        "
      >

        {/* Category / Badge */}
        <div className="mb-6">
          <span
            className="
              rounded-full
              border
              border-[#3651E0]/30
              px-4
              py-1.5
              font-[family-name:var(--font-mono)]
              text-sm
              font-semibold
              uppercase
              tracking-wide
              text-[#3651E0]
            "
          >
            Technology
          </span>
        </div>


        {/* Title */}
        <h1
          className="
            font-[family-name:var(--font-display)]
            text-4xl
            font-bold
            leading-tight
            tracking-tight
            text-[#14161A]
            md:text-5xl
          "
        >
          {post.title}
        </h1>


        {/* Author */}
        <div
          className="
            mt-6
            flex
            items-center
            gap-3
            text-sm
            text-[#8A8D93]
          "
        >
          <div
            className="
              flex
              h-10
              w-10
              items-center
              justify-center
              rounded-full
              bg-[#3651E0]
              font-bold
              text-[#FAFAF8]
            "
          >
            {post.author.username.charAt(0)}
          </div>

          <div>
            <p className="font-medium text-[#14161A]">
              {post.author.username}
            </p>
            <p>
              {post.published_at
                ? new Date(post.published_at).toLocaleDateString()
                : "No date"}
            </p>
          </div>
        </div>


        {/* Divider */}
        <div className="my-8 h-px bg-[#E4E4E0]" />


        {/* Content */}
        <div
          className="
            prose
            prose-lg
            max-w-none
            text-[#52565E]
            whitespace-pre-line
            prose-headings:font-[family-name:var(--font-display)]
            prose-headings:text-[#14161A]
          "
        >
          {post.content}
        </div>


        {/* Engagement Stats */}
        <div className="mt-8 flex items-center gap-6 border-t border-[#E4E4E0] pt-5 text-sm text-[#52565E]">
          <div className="flex items-center gap-3">
            <button
              onClick={() => handleReaction("like")}
              disabled={loadingReaction}
              className={`flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition
                ${
                  userReaction === "like"
                    ? "bg-blue-100 text-blue-600"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                }
              `}
              aria-label="Like post"
            >
              <ThumbsUp
                size={18}
                className={userReaction === "like" ? "fill-blue-600" : ""}
              />
              <span>{likes}</span>
            </button>

            <button
              onClick={() => handleReaction("dislike")}
              disabled={loadingReaction}
              className={`flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition
                ${
                  userReaction === "dislike"
                    ? "bg-red-100 text-red-600"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                }
              `}
              aria-label="Dislike post"
            >
              <ThumbsDown
                size={18}
                className={userReaction === "dislike" ? "fill-red-600" : ""}
              />
              <span>{dislikes}</span>
            </button>
          </div>

          <div className="flex items-center gap-1.5">
            <MessageCircle size={18} />
            <span>{commentCount}</span>
          </div>
        </div>

        {/* Comments Section */}
        <div className="mt-10 border-t border-[#E4E4E0] pt-6">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="font-[family-name:var(--font-display)] text-xl font-semibold text-[#14161A]">
              Comments
            </h2>

            <span className="text-sm text-[#8A8D93]">
              {commentCount}{" "}
              {commentCount === 1 ? "comment" : "comments"}
            </span>
          </div>

          <CommentForm
            onSubmit={(text) => handleAddComment(text)}
            loading={loadingComment}
          />

          {comments.length === 0 ? (
            <div className="rounded-lg border border-dashed border-[#E4E4E0] bg-[#F1F1EC] py-8 text-center">
              <p className="text-base font-medium text-[#14161A]">
                Be the first to comment!
              </p>
              <p className="mt-1 text-sm text-[#8A8D93]">
                No comments yet. Start the conversation.
              </p>
            </div>
          ) : (
            <div className="divide-y divide-[#E4E4E0]">
              {comments.map((comment) => (
                <CommentItem
                  key={comment.id}
                  comment={comment}
                />
              ))}
            </div>
          )}
        </div>

      </div>
    </article>
  );
}
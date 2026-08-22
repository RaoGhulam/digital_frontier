import { PostComment } from "@/types/post";

interface Props {
  comment: PostComment;
  depth?: number;
}

export default function CommentItem({
  comment,
  depth = 0,
}: Props) {
  return (
    <div className={depth > 0 ? "ml-6 border-l border-[#E4E4E0] pl-4" : ""}>
      <div className="py-4 border-b border-[#E4E4E0]">
        {/* Header */}
        <div className="flex items-center gap-3">
          {/* Avatar */}
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#F1F1EC] text-sm font-medium text-[#52565E]">
            {comment.user.username.charAt(0).toUpperCase()}
          </div>

          <div>
            <p className="text-sm font-medium text-[#14161A]">
              {comment.user.username}
            </p>

            <p className="font-[family-name:var(--font-mono)] text-xs text-[#8A8D93]">
              {new Date(comment.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>

        {/* Comment */}
        <p className="mt-3 text-sm leading-6 text-[#52565E]">
          {comment.content}
        </p>
      </div>

      {/* Replies */}
      {comment.replies?.length > 0 && (
        <div className="mt-2 space-y-2">
          {comment.replies.map((reply) => (
            <CommentItem
              key={reply.id}
              comment={reply}
              depth={depth + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
}
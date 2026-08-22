import { Post } from "@/types/post";
import Link from "next/link";

export default function PostCard({
  post,
}: {
  post: Post;
}) {
  return (
    <article
      className="
        group
        rounded-lg
        border
        border-[#E4E4E0]
        bg-[#FAFAF8]
        p-6
        shadow-[0_4px_20px_rgba(20,22,26,0.06)]
        transition
        duration-300
        hover:border-[#3651E0]/40
        hover:shadow-[0_8px_30px_rgba(20,22,26,0.10)]
      "
    >
      <div className="space-y-4">

        <span
          className="
            inline-block
            font-[family-name:var(--font-mono)]
            text-xs
            font-medium
            uppercase
            tracking-wider
            text-[#8A8D93]
          "
        >
          {post.category}
        </span>

        <h2
          className="
            font-[family-name:var(--font-display)]
            text-xl
            font-semibold
            leading-tight
            text-[#14161A]
            transition
            group-hover:text-[#3651E0]
          "
        >
          {post.title}
        </h2>

        <div
          className="
            flex
            gap-3
            text-sm
            text-[#8A8D93]
          "
        >
          <span>
            By {post.author_name}
          </span>

          <span>
            •
          </span>

          <time>
            {new Date(post.created_at).toLocaleDateString()}
          </time>
        </div>

        <div
          className="
            flex
            gap-5
            border-t
            border-[#E4E4E0]
            pt-4
            text-sm
            text-[#8A8D93]
          "
        >
          <span>👍 {post.likes}</span>
          <span>👎 {post.dislikes}</span>
          <span>💬 {post.comments}</span>
        </div>

        <Link
          href={`/posts/${post.slug}`}
          className="
            inline-flex
            items-center
            gap-2
            pt-2
            text-sm
            font-medium
            text-[#3651E0]
            transition
            hover:text-[#14161A]
          "
        >
          Read more →
        </Link>

      </div>
    </article>
  );
}
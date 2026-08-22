"use client";

import { useEffect, useState } from "react";
import { PostReviewModal } from "./PostReviewModal";

export interface PendingPost {
  id: number;
  author_id: number;
  title: string;
  slug: string;
  content: string;
  category: string;
  status: string;
  reviewed_by: number | null;
  reviewed_at: string | null;
  rejection_reason: string | null;
  published_at: string | null;
  created_at: string;
  updated_at: string;
}

interface Props {
  posts: PendingPost[];
  refreshPosts: () => Promise<void>;
}

const STORAGE_KEY = "pending-posts";

export default function PendingPostsTable({
  posts,
  refreshPosts,
}: Props) {
  const [selectedId, setSelectedId] = useState<number | null>(null);

  useEffect(() => {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(posts));
  }, [posts]);

  return (
    <>
      <div className="overflow-x-auto rounded-lg border">
        <table className="w-full text-sm">
          <thead className="bg-muted">
            <tr>
              <th className="p-3 text-left">Title</th>
              <th className="p-3 text-left">Category</th>
              <th className="p-3 text-left">Author ID</th>
              <th className="p-3 text-left">Created</th>
              <th className="p-3 text-left">Status</th>
            </tr>
          </thead>

          <tbody>
            {posts.map((post) => (
              <tr
                key={post.id}
                onClick={() => setSelectedId(post.id)}
                className="cursor-pointer border-t hover:bg-muted/50"
              >
                <td className="p-3 font-medium">{post.title}</td>
                <td className="p-3">{post.category}</td>
                <td className="p-3">{post.author_id}</td>
                <td className="p-3">
                  {new Date(post.created_at).toLocaleDateString()}
                </td>
                <td className="p-3 capitalize">{post.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <PostReviewModal
        postId={selectedId}
        open={selectedId !== null}
        onClose={() => setSelectedId(null)}
        refreshPosts={refreshPosts}
      />
    </>
  );
}
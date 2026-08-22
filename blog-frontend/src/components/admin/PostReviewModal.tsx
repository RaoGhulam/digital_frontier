"use client";

import { useEffect, useState } from "react";
import {
  approvePost,
  rejectPost,
} from "@/lib/api/pending_posts";

const STORAGE_KEY = "pending-posts";

interface Props {
  postId: number | null;
  open: boolean;
  onClose: () => void;
  refreshPosts: () => Promise<void>;
}

export function PostReviewModal({
  postId,
  open,
  onClose,
  refreshPosts,
}: Props) {
  const [post, setPost] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!postId) return;

    const stored = sessionStorage.getItem(STORAGE_KEY);

    if (!stored) return;

    const posts = JSON.parse(stored);

    const found = posts.find(
      (p: any) => p.id === postId
    );

    setPost(found);
  }, [postId]);


  const handleSuccess = async () => {
    await refreshPosts();

    sessionStorage.removeItem(STORAGE_KEY);

    onClose();
  };


  const approve = async () => {
    if (!post) return;

    try {
      setLoading(true);

      await approvePost(post.id);

      await handleSuccess();

    } catch (error) {
      console.error("Approve failed:", error);
    } finally {
      setLoading(false);
    }
  };


  const reject = async () => {
    if (!post) return;

    try {
      setLoading(true);

      await rejectPost(
        post.id,
        "Rejected by admin"
      );

      await handleSuccess();

    } catch (error) {
      console.error("Reject failed:", error);
    } finally {
      setLoading(false);
    }
  };


  if (!open || !post) return null;


  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-xl bg-white p-6">

        <div className="mb-5 flex justify-between">
          <h2 className="text-xl font-semibold">
            {post.title}
          </h2>

          <button
            onClick={onClose}
            disabled={loading}
          >
            ✕
          </button>
        </div>

        <div className="space-y-2 text-sm">
          <p><strong>ID:</strong> {post.id}</p>
          <p><strong>Author ID:</strong> {post.author_id}</p>
          <p><strong>Slug:</strong> {post.slug}</p>
          <p><strong>Category:</strong> {post.category}</p>
          <p><strong>Status:</strong> {post.status}</p>

          <p>
            <strong>Created:</strong>{" "}
            {new Date(post.created_at).toLocaleString()}
          </p>
        </div>


        <hr className="my-6" />


        <div>
          <h3 className="mb-2 font-semibold">
            Content
          </h3>

          <div className="max-h-96 overflow-y-auto rounded border p-4 whitespace-pre-wrap">
            {post.content}
          </div>
        </div>


        <div className="mt-6 flex justify-end gap-3">

          <button
            onClick={reject}
            disabled={loading}
            className="rounded bg-red-600 px-4 py-2 text-white"
          >
            {loading ? "Processing..." : "Reject"}
          </button>


          <button
            onClick={approve}
            disabled={loading}
            className="rounded bg-green-600 px-4 py-2 text-white"
          >
            {loading ? "Processing..." : "Approve"}
          </button>

        </div>

      </div>
    </div>
  );
}
"use client";

import { useState, FormEvent } from "react";
import { Send } from "lucide-react";

interface CommentFormProps {
  onSubmit: (text: string) => void;
  loading?: boolean;
}

export default function CommentForm({
  onSubmit,
  loading = false,
}: CommentFormProps) {
  const [comment, setComment] = useState("");

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!comment.trim()) return;

    onSubmit(comment);
    setComment("");
  };

  return (
    <form onSubmit={handleSubmit} className="mb-8">
      <div className="rounded-lg border border-[#E4E4E0] bg-white p-4">
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Write a comment..."
          rows={3}
          className="w-full resize-none bg-transparent text-sm text-[#14161A] outline-none placeholder:text-[#8A8D93]"
        />

        <div className="mt-3 flex justify-end">
          <button
            type="submit"
            disabled={loading || !comment.trim()}
            className="flex items-center gap-2 rounded-full bg-[#14161A] px-5 py-2 text-sm font-medium text-white transition hover:bg-[#2A2D32] disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Send size={16} />
            {loading ? "Posting..." : "Comment"}
          </button>
        </div>
      </div>
    </form>
  );
}
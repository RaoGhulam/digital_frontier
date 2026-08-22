"use client";

import { useState } from "react";
import { createPost, DuplicateSlugError } from "@/lib/api/create_post";

interface CreatePostModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export default function CreatePostModal({
  open,
  onClose,
  onSuccess,
}: CreatePostModalProps) {
  const [form, setForm] = useState({
    title: "",
    slug: "",
    content: "",
    category: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  if (!open) return null;

  function updateField(
    key: keyof typeof form,
    value: string
  ) {
    setForm((prev) => ({
      ...prev,
      [key]: value,
    }));
  }

  async function submitPost(
    e: React.FormEvent
  ) {
    e.preventDefault();

    setError("");
    setSuccess("");

    try {
      setLoading(true);

      const response = await createPost(form);

      setSuccess(response.message);

      onSuccess?.();

      setTimeout(() => {
        onClose();

        setForm({
          title: "",
          slug: "",
          content: "",
          category: "",
        });

        setSuccess("");
      }, 1000);

    } catch (err) {
      if (err instanceof DuplicateSlugError) {
        setError(
          "This slug already exists. Please choose another one."
        );
      } else {
        setError(
          err instanceof Error
            ? err.message
            : "Something went wrong"
        );
      }
    } finally {
      setLoading(false);
    }
  }


  return (
    <div className="
      fixed
      inset-0
      z-50
      flex
      items-center
      justify-center
      px-4
    ">
      <div className="
        w-full
        max-w-5xl
        rounded-xl
        bg-white
        p-6
        shadow-xl
      ">
        <div className="mb-5 flex justify-between">
          <h2 className="text-xl font-semibold">
            Create New Post
          </h2>

          <button
            onClick={onClose}
            className="text-gray-500"
          >
            ✕
          </button>
        </div>


        <form
          onSubmit={submitPost}
          className="space-y-4"
        >

          <input
            placeholder="Title"
            value={form.title}
            onChange={(e) =>
              updateField("title", e.target.value)
            }
            className="
              w-full
              rounded-lg
              border
              p-3
            "
            required
          />


          <input
            placeholder="Slug"
            value={form.slug}
            onChange={(e) =>
              updateField("slug", e.target.value)
            }
            className="
              w-full
              rounded-lg
              border
              p-3
            "
            required
          />


          <select
            value={form.category}
            onChange={(e) =>
              updateField("category", e.target.value)
            }
            className="
              w-full
              rounded-lg
              border
              p-3
            "
            required
          >
            <option value="" disabled>
              Select Category
            </option>
            <option value="Technology">Technology</option>
            <option value="Artificial Intelligence">
              Artificial Intelligence
            </option>
            <option value="Cyber Security">
              Cyber Security
            </option>
            <option value="Computer Science">
              Computer Science
            </option>
            <option value="FinTech">FinTech</option>
          </select>


          <textarea
            placeholder="Content"
            value={form.content}
            onChange={(e) =>
              updateField("content", e.target.value)
            }
            className="
              h-40
              w-full
              rounded-lg
              border
              p-3
            "
            required
          />


          {error && (
            <p className="text-sm text-red-600">
              {error}
            </p>
          )}

          {success && (
            <p className="text-sm text-green-600">
              {success}
            </p>
          )}


          <button
            disabled={loading}
            className="
              w-full
              rounded-lg
              bg-[#14161A]
              py-3
              text-white
              transition
              hover:bg-[#3651E0]
              disabled:opacity-50
            "
          >
            {loading
              ? "Creating..."
              : "Create Post"}
          </button>

        </form>
      </div>
    </div>
  );
}
"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
import CreatePostModal from "./post/CreatePostModal";

export default function AddPostButton() {
  const [openCreatePost, setOpenCreatePost] = useState(false);

  return (
    <>
      <div className="mb-10 flex justify-center">
        <button
          onClick={() => setOpenCreatePost(true)}
          className="
            inline-flex
            items-center
            gap-2
            rounded-lg
            bg-[#14161A]
            px-6
            py-3
            text-sm
            font-medium
            text-white
            shadow-[0_4px_20px_rgba(20,22,26,0.15)]
            transition
            hover:bg-[#3651E0]
          "
        >
          <span
            className="
              flex
              h-5
              w-5
              items-center
              justify-center
              rounded-full
              bg-white
              text-[#14161A]
            "
          >
            <Plus size={14} strokeWidth={3} />
          </span>

          Add New Post
        </button>
      </div>

      <CreatePostModal
        open={openCreatePost}
        onClose={() => setOpenCreatePost(false)}
      />
    </>
  );
}
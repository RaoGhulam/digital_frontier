"use client";

import { useEffect, useState } from "react";
import { getPosts } from "@/lib/api/pending_posts";
import PendingPostsTable from "@/components/admin/PendingPostsTable";

export default function Page() {
  const [posts, setPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadPosts = async () => {
    try {
      setLoading(true);

      const response = await getPosts();

      setPosts(response.data || []);
    } catch (error) {
      console.error("Failed to load posts:", error);
      setPosts([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPosts();
  }, []);

  if (loading && posts.length === 0) {
    return <div>Loading pending posts...</div>;
  }

  if (posts.length === 0) {
    return <div>No posts found</div>;
  }

  return (
    <main className="space-y-6 p-6">
      <PendingPostsTable
        posts={posts}
        refreshPosts={loadPosts}
      />
    </main>
  );
}
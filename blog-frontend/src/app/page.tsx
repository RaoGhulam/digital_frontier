import SectionHeader from "@/components/SectionHeader";
import PostFilters from "@/components/PostFilters";
import PostCard from "@/components/post/PostCard";
import AddPostButton from "@/components/AddPostButton";
import { getPosts } from "@/lib/api/home";
import { checkAuth } from "@/lib/auth";

interface Props {
  searchParams: Promise<{
    search?: string;
    category?: string;
    sort_by?: string;
    page?: string;
  }>;
}

export default async function Home({ searchParams }: Props) {
  const params = await searchParams;

  const [loggedIn, { posts, pagination }] = await Promise.all([
    checkAuth(),
    getPosts(params),
  ]);

  return (
    <main className="mx-auto max-w-7xl px-6">
      <section
        className="
          rounded-3xl
          border
          border-white/40
          bg-white/30
          p-8
          shadow-xl
          shadow-slate-200/40
          backdrop-blur-xl
        "
      >
        <SectionHeader />

        {loggedIn && <AddPostButton />}

        <PostFilters />

        <div
          className="
            mt-8
            grid
            gap-6
            md:grid-cols-2
            lg:grid-cols-3
          "
        >
          {posts.length === 0 ? (
            <p className="text-slate-500">
              No posts found.
            </p>
          ) : (
            posts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
              />
            ))
          )}
        </div>

        <div className="mt-10 flex items-center justify-center gap-4">
          {(() => {
            const prevParams = new URLSearchParams();
            const nextParams = new URLSearchParams();

            Object.entries(params).forEach(([key, value]) => {
              if (value) {
                prevParams.set(key, value);
                nextParams.set(key, value);
              }
            });

            prevParams.set("page", String(pagination.page - 1));
            nextParams.set("page", String(pagination.page + 1));

            return (
              <>
                {pagination.page > 1 && (
                  <a
                    href={`?${prevParams.toString()}`}
                    className="rounded-lg bg-slate-200 px-4 py-2"
                  >
                    Previous
                  </a>
                )}

                <span className="text-sm text-slate-500">
                  Page {pagination.page} of {pagination.total_pages}
                </span>

                {pagination.page < pagination.total_pages && (
                  <a
                    href={`?${nextParams.toString()}`}
                    className="rounded-lg bg-slate-200 px-4 py-2"
                  >
                    Next
                  </a>
                )}
              </>
            );
          })()}
        </div>
      </section>
    </main>
  );
}
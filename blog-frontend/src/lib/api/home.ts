import { PostsResponse } from "@/types/post";

const NEXT_PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL

export async function getPosts(params?: {
  search?: string;
  category?: string;
  sort_by?: string;
  page?: string;
}): Promise<PostsResponse> {

  const query = new URLSearchParams({
    category: params?.category ?? "all",
    sort_by: params?.sort_by ?? "latest",
    page: String(params?.page ?? 1),
  });

  if (params?.search) {
    query.append("search", params.search);
  }

  const res = await fetch(
    `${NEXT_PUBLIC_API_URL}/posts?${query.toString()}`,
    {
      next: {
        revalidate: 30,
      },
    }
  );

  if (!res.ok) {
    throw new Error("Failed fetching posts");
  }

  const data: PostsResponse = await res.json();

  return data;
}
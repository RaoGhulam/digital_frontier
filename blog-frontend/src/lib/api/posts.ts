import { cookies } from "next/headers";
import { PostDetail } from "@/types/post";

const NEXT_PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getPostBySlug(
  slug: string
): Promise<PostDetail> {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;

  const res = await fetch(
    `${NEXT_PUBLIC_API_URL}/posts/${slug}`,
    {
      headers: {
        Cookie: `access_token=${accessToken}`,
      },
      cache: "no-store",
    }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch post");
  }

  return res.json();
}
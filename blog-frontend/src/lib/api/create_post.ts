import {
  CreatePostPayload,
  CreatePostResponse,
} from "@/types/post";

const NEXT_PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL;

export class DuplicateSlugError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "DuplicateSlugError";
  }
}

export async function createPost(
  payload: CreatePostPayload
): Promise<CreatePostResponse> {
  const res = await fetch(
    `${NEXT_PUBLIC_API_URL}/posts/create`,
    {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );

  if (res.status === 409) {
    const error = await res.json();

    throw new DuplicateSlugError(
      error.message || "Slug already exists"
    );
  }

  if (!res.ok) {
    const error = await res.json();

    throw new Error(
      error.message || "Failed to create post"
    );
  }

  return res.json();
}
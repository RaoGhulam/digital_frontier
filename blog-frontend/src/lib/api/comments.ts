import {
  CreateCommentPayload,
  CommentResponse,
} from "@/types/comment";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function addComment(
  payload: CreateCommentPayload
): Promise<CommentResponse> {
  const response = await fetch(`${API_URL}/comments`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("UNAUTHORIZED");
    }

    throw new Error("FAILED_TO_ADD_COMMENT");
  }

  return response.json();
}
import { ReactionRequest, ReactionResponse } from "@/types/reaction";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function reactToPost(
  body: ReactionRequest
): Promise<ReactionResponse> {
  const res = await fetch(`${API_URL}/reactions/reaction`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  if (res.status === 401) {
    throw new Error("UNAUTHORIZED");
  }

  if (!res.ok) {
    const error = await res.text();
    console.error("Reaction API error:", error);
    throw new Error("Failed to react");
  }

  return res.json();
}
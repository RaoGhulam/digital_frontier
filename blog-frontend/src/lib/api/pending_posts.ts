const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getPosts() {
  const res = await fetch(`${API_URL}/admin/pending-posts`, {
    method: "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
  });

  if (!res.ok) {
    return {
      status: "error",
      data: [],
    };
  }

  return res.json();
}

interface ModeratePostPayload {
  action: "approve" | "reject";
  rejection_reason?: string | null;
}

export async function moderatePost(
  pendingPostId: number,
  payload: ModeratePostPayload
) {
  const res = await fetch(
    `${API_URL}/admin/moderate-post/${pendingPostId}`,
    {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );

  if (!res.ok) {
    throw new Error("Failed to moderate post");
  }

  return res.json();
}

export async function approvePost(pendingPostId: number) {
  return moderatePost(pendingPostId, {
    action: "approve",
  });
}

export async function rejectPost(
  pendingPostId: number,
  rejection_reason: string
) {
  return moderatePost(pendingPostId, {
    action: "reject",
    rejection_reason,
  });
}
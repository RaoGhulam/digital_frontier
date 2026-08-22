import type { LoginRequest } from "@/types/auth";

const NEXT_PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function login(payload: LoginRequest) {
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
    credentials: "include",
  });

  const data = await response.json();

  if (response.status === 429) {
    throw new Error("Too many login attempts. Please try again later.");
  }

  if (!response.ok) {
    throw new Error(data.message || "Incorrect email or password");
  }

  return data;
}

export async function signup({
  username,
  email,
  password,
}: {
  username: string;
  email: string;
  password: string;
}) {
  const res = await fetch(`${NEXT_PUBLIC_API_URL}/users/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      email,
      password,
    }),
  });

  if (res.status !== 201) {
    const data = await res.json().catch(() => null);

    throw new Error(data?.message || "Failed to create account");
  }

  return await res.json();
}

export async function verifyEmail(token: string) {
  if (!NEXT_PUBLIC_API_URL) {
    throw new Error("API URL is not configured.");
  }

  const response = await fetch(
    `${NEXT_PUBLIC_API_URL}/users/verify-email?token=${encodeURIComponent(token)}`,
    {
      method: "GET",
    }
  );

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      data?.detail ||
        data?.message ||
        "Unable to verify your email."
    );
  }

  return data;
}

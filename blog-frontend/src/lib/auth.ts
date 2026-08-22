import { cookies } from "next/headers";

export async function checkAuth() {
  const cookieStore = await cookies();

  const token = cookieStore.get("access_token");

  return Boolean(token);
}
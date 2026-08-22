import { NextResponse } from "next/server";

const ADMIN_API_URL = process.env.API_ADMIN_LOGIN_URL;
const USER_API_URL = process.env.API_USER_LOGIN_URL;

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const { email } = body;

    // Choose API based on email
    const apiUrl = email?.toLowerCase().endsWith("@admin.com")
      ? ADMIN_API_URL
      : USER_API_URL;

    if (!apiUrl) {
      return NextResponse.json(
        { message: "Login API is not configured" },
        { status: 500 }
      );
    }

    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      return NextResponse.json(
        {
          message:
            response.status === 429
              ? "Too many login attempts. Please try again later."
              : "Incorrect email or password",
        },
        {
          status: response.status,
        }
      );
    }

    const data = await response.json();

    console.log("Backend access token:", data.access_token);
    const result = NextResponse.json(
      {
        success: true,
      },
      {
        status: 200,
      }
    );

    result.cookies.set("access_token", data.access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      path: "/",
      maxAge: 60 * 60 * 24, // 24 hours
    });

    return result;
  } catch (error) {
    return NextResponse.json(
      {
        message: "Something went wrong",
      },
      {
        status: 500,
      }
    );
  }
}
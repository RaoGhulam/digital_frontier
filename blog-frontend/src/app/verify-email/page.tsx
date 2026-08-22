"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { verifyEmail } from "@/lib/api/auth";

type Status = "verifying" | "success" | "error";

export default function VerifyEmailPage() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  const [status, setStatus] = useState<Status>("verifying");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("Verification token is missing.");
      return;
    }

    const verify = async () => {
      try {
        const data = await verifyEmail(token);

        setStatus("success");
        setMessage(data.message);
      } catch (error) {
        setStatus("error");

        setMessage(
          error instanceof Error
            ? error.message
            : "Something went wrong. Please try again."
        );
      }
    };

    verify();
  }, [token]);

  if (status === "verifying") {
    return (
      <main>
        <h1>Verifying your email...</h1>
        <p>Please wait.</p>
      </main>
    );
  }

  if (status === "error") {
    return (
      <main>
        <h1>Verification failed</h1>
        <p>{message}</p>
      </main>
    );
  }

  return (
    <main>
      <h1>Email verified!</h1>
      <p>You can now try logging in to your account.</p>
    </main>
  );
}

"use client";

import { useState } from "react";
import { signup } from "@/lib/api/auth";

interface SignupFormProps {
  onSuccess?: () => void;
}

export default function SignupForm({ onSuccess }: SignupFormProps) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    setLoading(true);
    setError("");

    try {
        await signup({
            username,
            email,
            password,
        });

        alert("Account created! Please check your email to verify your account.");

        onSuccess?.();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Signup failed"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="w-full space-y-6"
    >
      <h2 className="text-2xl font-semibold">
        Create Account
      </h2>

      {error && (
        <div className="rounded bg-red-100 px-3 py-2 text-sm text-red-600">
          {error}
        </div>
      )}

      <div>
        <label className="mb-1 block text-sm">
          Username
        </label>

        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          className="w-full rounded border px-3 py-2"
          placeholder="Username"
        />
      </div>

      <div>
        <label className="mb-1 block text-sm">
          Email
        </label>

        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full rounded border px-3 py-2"
          placeholder="email@example.com"
        />
      </div>

      <div>
        <label className="mb-1 block text-sm">
          Password
        </label>

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full rounded border px-3 py-2"
          placeholder="Password"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="
          w-full
          rounded
          bg-black
          px-4
          py-2
          text-white
          disabled:opacity-50
        "
      >
        {loading ? "Creating..." : "Sign Up"}
      </button>
    </form>
  );
}
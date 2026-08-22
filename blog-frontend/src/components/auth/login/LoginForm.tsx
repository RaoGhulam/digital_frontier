"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/lib/api/auth";
import { Eye, EyeOff } from "lucide-react";

interface LoginFormProps {
  onSuccess?: () => void;
  onSignupClick?: () => void;
}

export default function LoginForm({
  onSuccess,
  onSignupClick,
}: LoginFormProps) {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  async function handleSubmit(
    e: React.FormEvent<HTMLFormElement>
  ) {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      await login({
        email,
        password,
      });

      // Close the modal
      onSuccess?.();

      // Refresh the current page so auth state updates
      router.refresh();

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Incorrect email or password"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="
        w-full
        space-y-6
      "
    >
      <h2 className="text-2xl font-semibold">
        Login
      </h2>

      {error && (
        <div
          className="
            rounded
            bg-red-100
            px-3
            py-2
            text-sm
            text-red-600
          "
        >
          {error}
        </div>
      )}

      <div>
        <label className="mb-1 block text-sm">
          Email
        </label>

        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="email@example.com"
          required
          className="
            w-full
            rounded
            border
            px-3
            py-2
          "
        />
      </div>

      <div>
        <label className="mb-1 block text-sm">
          Password
        </label>

        <div className="relative">
          <input
            type={showPassword ? "text" : "password"}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
            className="
              w-full
              rounded
              border
              px-3
              py-2
              pr-10
            "
          />

          <button
            type="button"
            onClick={() => setShowPassword((prev) => !prev)}
            className="
              absolute
              right-3
              top-1/2
              -translate-y-1/2
              text-gray-500
              hover:text-gray-700
            "
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
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
        {loading ? "Logging in..." : "Login"}
      </button>

      <p className="text-center text-sm text-gray-600">
        Don't have an account?{" "}
        <button
          type="button"
          onClick={onSignupClick}
          className="font-medium text-black underline"
        >
          Sign up
        </button>
      </p>
    </form>
  );
}
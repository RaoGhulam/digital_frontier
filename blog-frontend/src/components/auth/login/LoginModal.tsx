"use client";

import LoginForm from "./LoginForm";

interface LoginModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
  onSignupClick: () => void;
}

export default function LoginModal({
  open,
  onClose,
  onSuccess,
  onSignupClick,
}: LoginModalProps) {
  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      onClick={onClose}
    >
      <div
        className="
          relative
          w-full
          max-w-lg
          rounded-xl
          bg-white
          p-8
          shadow-xl
        "
        onClick={(e) => e.stopPropagation()}
      >
        <button
          className="absolute right-3 top-3"
          onClick={onClose}
        >
          ✕
        </button>

        <LoginForm
          onSuccess={onSuccess}
          onSignupClick={onSignupClick}
        />
      </div>
    </div>
  );
}
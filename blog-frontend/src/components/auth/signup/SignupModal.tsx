"use client";

import SignupForm from "./SignupForm";

interface SignupModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function SignupModal({
  open,
  onClose,
  onSuccess,
}: SignupModalProps) {
  if (!open) return null;

  return (
    <div
      className="
        fixed
        inset-0
        z-50
        flex
        items-center
        justify-center
        bg-black/50
      "
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

        <SignupForm onSuccess={onSuccess} />
      </div>
    </div>
  );
}
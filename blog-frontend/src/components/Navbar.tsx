"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import LoginModal from "./auth/login/LoginModal";
import SignupModal from "./auth/signup/SignupModal";

export default function Navbar() {
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const router = useRouter();

  const navItems = [
    { name: "Home", href: "/" },
    { name: "About", href: "/about" },
    { name: "Contact", href: "/contact" },
  ];

  const buttonClass = `
    relative
    cursor-pointer
    text-white
    transition-colors
    duration-300
    hover:text-[#6E86FF]
    after:absolute
    after:-bottom-1
    after:left-0
    after:h-[2px]
    after:w-0
    after:bg-[#6E86FF]
    after:transition-all
    hover:after:w-full
  `;

  useEffect(() => {
    async function checkAuth() {
      try {
        const res = await fetch("/api/auth/me");
        const data = await res.json();
        setLoggedIn(data.authenticated);
      } catch {
        setLoggedIn(false);
      }
    }

    checkAuth();
  }, []);

  async function handleLogout() {
    await fetch("/api/auth/logout", {
      method: "POST",
    });

    setLoggedIn(false);
    setMobileOpen(false);
    localStorage.clear();
    router.refresh();
  }

  return (
    <>
      <nav
        className="
          top-0
          z-50
          mx-4
          mt-4
          w-[calc(100%_-_2rem)]
          rounded-2xl
          border
          border-[#2A2D35]
          bg-[#14161A]
        "
      >
        <div
          className="
            mx-auto
            flex
            h-16
            max-w-7xl
            items-center
            justify-between
            px-4
            sm:px-6
          "
        >
          {/* Logo */}
          <Link
            href="/"
            className="
              font-[family-name:var(--font-display)]
              text-xl
              font-bold
              tracking-tight
              text-white
            "
          >
            Digital Frontier
          </Link>

          {/* Desktop Menu */}
          <div
            className="
              hidden
              items-center
              gap-8
              font-[family-name:var(--font-mono)]
              text-[13px]
              uppercase
              tracking-wide
              md:flex
            "
          >
            {navItems.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="
                  relative
                  text-white
                  transition-colors
                  duration-300
                  hover:text-[#6E86FF]
                  after:absolute
                  after:-bottom-1
                  after:left-0
                  after:h-[2px]
                  after:w-0
                  after:bg-[#6E86FF]
                  after:transition-all
                  hover:after:w-full
                "
              >
                {item.name}
              </Link>
            ))}

            {loggedIn ? (
              <button
                onClick={handleLogout}
                className={buttonClass}
              >
                Logout
              </button>
            ) : (
              <button
                onClick={() => setShowLogin(true)}
                className={buttonClass}
              >
                Login
              </button>
            )}
          </div>

          {/* Mobile Hamburger */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="
              flex
              flex-col
              gap-1.5
              md:hidden
            "
            aria-label="Toggle menu"
          >
            <span
              className={`
                h-[2px]
                w-6
                bg-white
                transition
                ${
                  mobileOpen
                    ? "translate-y-2 rotate-45"
                    : ""
                }
              `}
            />

            <span
              className={`
                h-[2px]
                w-6
                bg-white
                transition
                ${
                  mobileOpen
                    ? "opacity-0"
                    : ""
                }
              `}
            />

            <span
              className={`
                h-[2px]
                w-6
                bg-white
                transition
                ${
                  mobileOpen
                    ? "-translate-y-2 -rotate-45"
                    : ""
                }
              `}
            />
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileOpen && (
          <div
            className="
              flex
              flex-col
              gap-5
              border-t
              border-[#2A2D35]
              px-6
              py-5
              font-[family-name:var(--font-mono)]
              text-[13px]
              uppercase
              tracking-wide
              md:hidden
            "
          >
            {navItems.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                onClick={() => setMobileOpen(false)}
                className="
                  text-white
                  transition-colors
                  hover:text-[#6E86FF]
                "
              >
                {item.name}
              </Link>
            ))}

            {loggedIn ? (
              <button
                onClick={handleLogout}
                className={`${buttonClass} text-left`}
              >
                Logout
              </button>
            ) : (
              <button
                onClick={() => {
                  setShowLogin(true);
                  setMobileOpen(false);
                }}
                className={`${buttonClass} text-left`}
              >
                Login
              </button>
            )}
          </div>
        )}
      </nav>

      <LoginModal
        open={showLogin}
        onClose={() => setShowLogin(false)}
        onSignupClick={() => {
          setShowLogin(false);
          setShowSignup(true);
        }}
        onSuccess={() => {
          setLoggedIn(true);
          setShowLogin(false);
          router.refresh();
        }}
      />

      <SignupModal
        open={showSignup}
        onClose={() => setShowSignup(false)}
        onSuccess={() => {
          setShowSignup(false);
          setShowLogin(true);
        }}
      />
    </>
  );
}
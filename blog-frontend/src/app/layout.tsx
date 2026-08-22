import "./globals.css";
import Navbar from "@/components/Navbar";

import { Space_Grotesk, Inter, IBM_Plex_Mono } from "next/font/google";

const display = Space_Grotesk({
  subsets: ["latin"],
  weight: ["500", "700"],
  variable: "--font-display",
});

const body = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-body",
});

const mono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono",
});

export const metadata = {
  title: "Digital Frontier",
  description: "Technology, AI and innovation blog",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${display.variable} ${body.variable} ${mono.variable}`}
    >
      <body
        className="
          min-h-screen
          bg-[#FAFAF8]
          text-[#14161A]
          antialiased
          font-[family-name:var(--font-body)]
        "
      >
        <div className="relative min-h-screen overflow-hidden">

          {/* Background */}
          <div
            className="
              absolute inset-0
              bg-[radial-gradient(circle,rgba(20,22,26,0.07)_1px,transparent_1px)]
              bg-[length:22px_22px]
            "
          />

          {/* Navbar above all pages */}
          <Navbar />

          <main className="relative mx-auto min-h-screen max-w-7xl px-6 py-2">
            {children}
          </main>

        </div>
      </body>
    </html>
  );
}
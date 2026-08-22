"use client";

import { useRouter, useSearchParams } from "next/navigation";

export default function PostFilters() {
  const router = useRouter();
  const params = useSearchParams();

  function update(key: string, value: string) {
    const query = new URLSearchParams(params.toString());

    if (value) {
      query.set(key, value);
    } else {
      query.delete(key);
    }

    router.push(`/?${query.toString()}`);
  }

  return (
    <div className="grid gap-4 mb-10 md:grid-cols-3">

      <input
        defaultValue={params.get("search") ?? ""}
        onChange={(e) => update("search", e.target.value)}
        placeholder="Search posts..."
        className="
          rounded-lg
          border
          border-[#E4E4E0]
          bg-[#FAFAF8]
          px-5
          py-3
          text-[#14161A]
          placeholder:text-[#9A9DA3]
          outline-none
          transition
          focus:border-[#3651E0]
          focus:ring-2
          focus:ring-[#3651E0]/20
        "
      />

      <select
        value={params.get("category") ?? ""}
        onChange={(e) => update("category", e.target.value)}
        className="
          rounded-lg
          border
          border-[#E4E4E0]
          bg-[#FAFAF8]
          px-5
          py-3
          text-[#52565E]
          outline-none
          transition
          focus:border-[#3651E0]
          focus:ring-2
          focus:ring-[#3651E0]/20
        "
      >
        <option value="">
          All Categories
        </option>

        <option value="Technology">
          Technology
        </option>

        <option value="Artificial Intelligence">
          Artificial Intelligence
        </option>

        <option value="Cyber Security">
          Cyber Security
        </option>

        <option value="FinTech">
          FinTech
        </option>

        <option value="Computer Science">
          Computer Science
        </option>
      </select>

      <select
        value={params.get("sort_by") ?? ""}
        onChange={(e) => update("sort_by", e.target.value)}
        className="
          rounded-lg
          border
          border-[#E4E4E0]
          bg-[#FAFAF8]
          px-5
          py-3
          text-[#52565E]
          outline-none
          transition
          focus:border-[#3651E0]
          focus:ring-2
          focus:ring-[#3651E0]/20
        "
      >
        <option value="" disabled>
          Sort By
        </option>

        <option value="latest">
          Latest
        </option>

        <option value="oldest">
          Oldest
        </option>
      </select>

    </div>
  );
}
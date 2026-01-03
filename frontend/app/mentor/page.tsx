"use client";

import {useRouter} from "next/navigation";
import MentorChat from "@/components/MentorChat";

export default function MentorPage(){
  const router=useRouter();

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-semibold mb-4">
          CP Mentor 🤖
        </h1>

        <p className="text-gray-600 mb-6">
          Ask questions about your weak topics, problem solving strategies,
          or competitive programming in general.
        </p>

        <MentorChat />

        <div className="mt-6">
          <button
            onClick={() => router.push("/dashboard")}
            className="text-blue-600 hover:underline"
          >
            ← Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}
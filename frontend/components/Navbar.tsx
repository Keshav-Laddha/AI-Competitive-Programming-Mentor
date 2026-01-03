"use client";

import Link from "next/link";
import {useRouter, usePathname} from "next/navigation";
import {logout} from "@/lib/auth";

export default function Navbar(){
  const router=useRouter();
  const pathname=usePathname();

  //hide navbar on auth pages
  if (pathname==="/login" || pathname==="/register"){
    return null;
  }

  return (
    <nav className="w-full bg-gray-900 text-white px-6 py-3 flex justify-between items-center">
      {/* Left: App Name */}
      <Link href="/dashboard" className="font-semibold text-lg">
        CP Mentor
      </Link>

      {/* Center: Navigation */}
      <div className="flex gap-6 text-sm">
        <Link href="/dashboard" className="hover:text-gray-300">
          Dashboard
        </Link>
        <Link href="/sync" className="hover:text-gray-300">
          Sync
        </Link>
        <Link href="/mentor" className="hover:text-gray-300">
          Mentor
        </Link>
      </div>

      {/* Right: Logout */}
      <button
        onClick={()=>logout()}
        className="text-sm bg-red-600 px-3 py-1 rounded hover:bg-red-700"
      >
        Logout
      </button>
    </nav>
  );
}
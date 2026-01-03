"use client";

import {useState} from "react";
import {useRouter} from "next/navigation";
import {apiRequest} from "@/lib/api";

export default function RegisterPage(){
  const router=useRouter();
  const [email, setEmail]=useState("");
  const [password, setPassword]=useState("");
  const [displayName, setDisplayName]=useState("");
  const [error, setError]=useState("");
  const [loading, setLoading]=useState(false);

  async function handleRegister(e: React.FormEvent){
    e.preventDefault();
    setError("");
    setLoading(true);

    try{
      await apiRequest("/auth/register", {method: "POST", body: JSON.stringify({email, password, display_name: displayName})});
      router.push("/login");
    }
    catch (err: any){
      setError(err.message);
    }
    finally{
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleRegister}
        className="bg-white p-6 rounded shadow w-96"
      >
        <h1 className="text-xl font-semibold mb-4">Register</h1>

        {error && <p className="text-red-500 mb-2">{error}</p>}

        <input
          className="w-full mb-3 p-2 border rounded"
          type="text"
          placeholder="Display Name"
          value={displayName}
          onChange={e => setDisplayName(e.target.value)}
        />

        <input
          className="w-full mb-3 p-2 border rounded"
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />

        <input
          className="w-full mb-4 p-2 border rounded"
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />

        <button
          disabled={loading}
          className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700"
        >
          {loading ? "Creating..." : "Register"}
        </button>

        <p className="mt-3 text-sm text-center">
          Already have an account?{" "}
          <a href="/login" className="text-blue-600">
            Login
          </a>
        </p>
      </form>
    </div>
  );
}
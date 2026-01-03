"use client";

import {useState} from "react";
import {useRouter} from "next/navigation";
import {apiRequest} from "@/lib/api";
import {setToken} from "@/lib/auth";

export default function LoginPage(){
  const router=useRouter();
  const [email, setEmail]=useState("");
  const [password, setPassword]=useState("");
  const [error, setError]=useState("");
  const [loading, setLoading]=useState(false);

  async function handleLogin(e: React.FormEvent){
    e.preventDefault();
    setError("");
    setLoading(true);

    try{
      const data=await apiRequest("/auth/login",{method: "POST", body: JSON.stringify({email, password})});
      setToken(data.access_token);
      router.push("/dashboard");
    }
    catch (err: any){
      setError(err.message);
    }
    finally{
      setLoading(false);
    }
  }

  return(
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleLogin}
        className="bg-white p-6 rounded shadow w-96"
      >
        <h1 className="text-xl font-semibold mb-4">Login</h1>

    {error && <p className="text-red-500 mb-2">{error}</p>}

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
          className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
        >
        {loading ? "Logging in..." : "Login"}
        </button>

        <p className="mt-3 text-sm text-center">
          Don’t have an account?{" "}
          <a href="/register" className="text-blue-600">
            Register
          </a>
        </p>
      </form>
    </div>
  );
}
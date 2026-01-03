"use client";

import {useEffect, useState} from "react";
import {apiRequest} from "@/lib/api";

type Handle={
  id: string;
  platform: string;
  handle: string;
  last_synced_at?: string;
};

export default function SyncPage(){
  const [handles, setHandles]=useState<Handle[]>([]);
  const [platform, setPlatform]=useState("codeforces");
  const [handle, setHandle]=useState("");
  const [loading, setLoading]=useState(false);
  const [message, setMessage]=useState("");

  async function fetchHandles(){
    const data=await apiRequest("/handles");
    setHandles(data);
  }

  useEffect(()=>{
    fetchHandles();
  }, []);

  async function addHandle(e: React.FormEvent){
    e.preventDefault();
    setMessage("");
    setLoading(true);

    try{
      await apiRequest("/handles", {method: "POST", body: JSON.stringify({platform, handle})});
      setHandle("");
      await fetchHandles();
      setMessage("Handle added successfully");
    }
    catch(err: any){
      setMessage(err.message);
    }
    finally{
      setLoading(false);
    }
  }

  async function syncHandle(id: string) {
    setMessage("");
    try
    {
      await apiRequest(`/handles/${id}/sync`, {method: "POST"});
      setMessage("Sync started in background");
    }
    catch(err: any){
      setMessage(err.message);
    }
  }

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-semibold mb-6">Sync CP Handles</h1>

      {/* Add Handle */}
      <form
        onSubmit={addHandle}
        className="bg-white p-4 rounded shadow mb-6 max-w-md"
      >
        <h2 className="font-medium mb-3">Add New Handle</h2>

        <select
          className="w-full mb-3 p-2 border rounded"
          value={platform}
          onChange={e => setPlatform(e.target.value)}
        >
          <option value="codeforces">Codeforces</option>
        </select>

        <input
          className="w-full mb-3 p-2 border rounded"
          placeholder="Handle"
          value={handle}
          onChange={e => setHandle(e.target.value)}
          required
        />

        <button
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          {loading ? "Adding..." : "Add Handle"}
        </button>
      </form>

      {/* Messages */}
      {message && (
        <p className="mb-4 text-sm text-gray-700">{message}</p>
      )}

      {/* Existing Handles */}
      <div className="bg-white p-4 rounded shadow max-w-md">
        <h2 className="font-medium mb-3">Connected Handles</h2>

        {handles.length === 0 ? (
          <p className="text-gray-600">No handles connected yet.</p>
        ) : (
          <ul className="space-y-3">
            {handles.map(h => (
              <li
                key={h.id}
                className="flex justify-between items-center border p-3 rounded"
              >
                <div>
                  <div className="font-medium">
                    {h.platform} — {h.handle}
                  </div>
                  <div className="text-xs text-gray-500">
                    Last synced:{" "}
                    {h.last_synced_at
                      ? new Date(h.last_synced_at).toLocaleString()
                      : "Never"}
                  </div>
                </div>

                <button
                  onClick={() => syncHandle(h.id)}
                  className="text-sm bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
                >
                  Sync
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
import {getToken} from "./auth";

const BASE_URL="http://localhost:8000"; //backend

export async function apiRequest(path: string, options: RequestInit={}){
  const token=getToken();

  const headers: HeadersInit={
    "Content-Type": "application/json",
    ...(token ? {Authorization: `Bearer ${token}`}:{}),
    ...(options.headers || {})
  };

  const res=await fetch(`${BASE_URL}${path}`, {...options, headers});

  if(!res.ok){
    const error=await res.json();
    throw new Error(error.detail || "Something went wrong");
  }

  return res.json();
}
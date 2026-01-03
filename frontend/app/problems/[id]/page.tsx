"use client";

import {useEffect, useState} from "react";
import {useParams} from "next/navigation";
import {apiRequest} from "@/lib/api";
import MentorChat from "@/components/MentorChat";

export default function ProblemPage() {
  const {id}=useParams();
  const [problem, setProblem]=useState<any>(null);
  const [loading, setLoading]=useState(true);
  const [error, setError]=useState("");

  useEffect(()=>{
    async function fetchProblem(){
      try{
        const data=await apiRequest(`/problems/${id}`);
        setProblem(data);
      }
      catch (err: any){
        setError(err.message);
      }
      finally{
        setLoading(false);
      }
    }

    fetchProblem();
  }, [id]);

  if(loading) return <p className="p-6">Loading problem...</p>;
  if(error) return <p className="p-6 text-red-500">{error}</p>;
  if(!problem) return null;

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-semibold mb-2">{problem.title}</h1>

      <div className="text-sm text-gray-600 mb-4">
        Difficulty: {problem.difficulty}
      </div>

      <div className="flex gap-2 mb-6">
        {problem.tags.map((tag: string) => (
          <span
            key={tag}
            className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded"
          >
            {tag}
          </span>
        ))}
      </div>

      <div className="bg-white p-4 rounded shadow mb-6 whitespace-pre-wrap">
        {problem.statement}
      </div>

      <MentorChat problemId={problem.id} />
    </div>
  );
}
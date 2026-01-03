"use client";

import {useEffect, useState} from "react";
import {useRouter} from "next/navigation";
import {apiRequest} from "@/lib/api";
import WeakTopicCard from "@/components/WeakTopicCard";
import RecommendationCard from "@/components/RecommendationCard";

export default function DashboardPage(){
  const router=useRouter();
  const [weakTopics, setWeakTopics]=useState<Record<string, number>>({});
  const [recommendations, setRecommendations]=useState<any[]>([]);
  const [loading, setLoading]=useState(true);
  const [error, setError]=useState("");

  useEffect(()=>{
    async function fetchDashboard(){
      try{
        const topics=await apiRequest("/analysis/weak-topics");
        const recs=await apiRequest("/recommendations/latest");
        setWeakTopics(topics);
        setRecommendations(recs);
      }
      catch (err: any){
        setError(err.message);
        if (err.message.includes("token")){
          router.push("/login");
        }
      }
      finally{
        setLoading(false);
      }
    }
    fetchDashboard();
  }, [router]);

  if(loading){
    return <p className="p-6">Loading dashboard...</p>;
  }

  if(error){
    return <p className="p-6 text-red-500">{error}</p>;
  }

  return(
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-semibold mb-6">Dashboard</h1>

      {/* Weak Topics */}
      <section className="mb-8">
        <h2 className="text-lg font-medium mb-4">Weak Topics</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(weakTopics).map(([topic, value]) => (
            <WeakTopicCard
              key={topic}
              topic={topic}
              weakness={value}
            />
          ))}
        </div>
      </section>

      {/* Recommendations */}
      <section className="mb-8">
        <h2 className="text-lg font-medium mb-4">
          Today’s Recommendations
        </h2>

        {recommendations.length === 0 ? (
          <p className="text-gray-600">
            No recommendations yet. Sync your CP handle.
          </p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendations.map(problem => (
              <RecommendationCard
                key={problem.id}
                problem={problem}
              />
            ))}
          </div>
        )}
      </section>

      {/* Mentor CTA */}
      <section>
        <button
          onClick={() => router.push("/mentor")}
          className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
        >
          Ask Mentor 🤖
        </button>
      </section>
    </div>
  );
}
"use client";

import {useState} from "react";
import {apiRequest} from "@/lib/api";
import ChatMessage from "./ChatMessage";

type Message={
  role: "user" | "mentor";
  content: string;
};

type Props={
  problemId?: string;
};

export default function MentorChat({ problemId }: Props){
  const [messages, setMessages]=useState<Message[]>([]);
  const [input, setInput]=useState("");
  const [loading, setLoading]=useState(false);

  async function sendMessage(){
    if(!input.trim()) return;

    const userMessage: Message={
      role: "user",
      content: input
    };

    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try{
      const res=await apiRequest("/mentor/chat", {
        method: "POST",
        body: JSON.stringify({
          question: userMessage.content,
          problem_id: problemId || null
        })
      });

      setMessages(prev=>[
        ...prev,
        { role: "mentor", content: res.reply }
      ]);
    }
    catch(err){
      setMessages(prev=>[
        ...prev,
        {
          role: "mentor",
          content: "Something went wrong. Please try again."
        }
      ]);
    }
    finally{
      setLoading(false);
    }
  }

  return (
    <div className="border rounded p-4 bg-white">
      <h3 className="font-medium mb-3">Ask Mentor 🤖</h3>

      <div className="flex flex-col gap-3 mb-3 max-h-80 overflow-y-auto">
        {messages.map((m, i) => (
          <ChatMessage key={i} role={m.role} content={m.content} />
        ))}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 border rounded p-2"
          placeholder="Ask a question..."
          value={input}
          onChange={e => setInput(e.target.value)}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-purple-600 text-white px-4 rounded hover:bg-purple-700"
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}
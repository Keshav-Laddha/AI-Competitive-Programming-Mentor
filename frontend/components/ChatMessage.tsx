type Props={role: "user" | "mentor"; content: string;};

export default function ChatMessage({ role, content }: Props) {
  const isUser= role==="user";

  return (
    <div
      className={`p-3 rounded max-w-xl ${
        isUser
          ? "bg-blue-600 text-white self-end"
          : "bg-gray-200 text-gray-900 self-start"
      }`}
    >
      {content}
    </div>
  );
}
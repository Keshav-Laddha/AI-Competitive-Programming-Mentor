import Link from "next/link";

type Props={
  problem:{
    id: string;
    title: string;
    difficulty: number;
    tags: string[];
  };
};

export default function RecommendationCard({ problem }: Props) {
  return (
    <div className="p-4 border rounded bg-white shadow-sm">
      <h3 className="font-semibold mb-1">{problem.title}</h3>

      <div className="text-sm text-gray-600 mb-2">
        Difficulty: {problem.difficulty}
      </div>

      <div className="flex gap-2 flex-wrap mb-3">
        {problem.tags.map(tag => (
          <span
            key={tag}
            className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded"
          >
            {tag}
          </span>
        ))}
      </div>

      <Link
        href={`/problems/${problem.id}`}
        className="text-sm text-blue-600 hover:underline"
      >
        Solve →
      </Link>
    </div>
  );
}
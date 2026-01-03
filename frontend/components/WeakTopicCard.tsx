type Props={topic: string; weakness: number;};

export default function WeakTopicCard({ topic, weakness }: Props){
  const percent=Math.round(weakness*100);

  return(
    <div className="p-4 border rounded bg-white shadow-sm">
      <div className="flex justify-between mb-2">
        <span className="font-medium capitalize">{topic}</span>
        <span className="text-sm text-gray-500">{percent}%</span>
      </div>

      <div className="w-full bg-gray-200 h-2 rounded">
        <div
          className="bg-red-500 h-2 rounded"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
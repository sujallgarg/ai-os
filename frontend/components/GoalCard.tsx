import Link from "next/link";

interface GoalCardProps {
  job: {
    id: string;
    goal: string;
    status: string;
    progress: number;
  };
}

export default function GoalCard({
  job
}: GoalCardProps) {

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

      <div className="flex items-start justify-between gap-4">

        <div>

          <p className="text-xs font-semibold uppercase tracking-wider text-indigo-600">
            Active Goal
          </p>

          <h3 className="mt-2 text-lg font-semibold text-slate-950">
            {job.goal}
          </h3>

        </div>

        <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700">
          {job.status}
        </span>

      </div>


      <div className="mt-6">

        <div className="mb-2 flex justify-between text-sm">

          <span className="text-slate-500">
            Progress
          </span>

          <span className="font-semibold text-slate-900">
            {job.progress}%
          </span>

        </div>


        <div className="h-2 overflow-hidden rounded-full bg-slate-100">

          <div
            className="h-full rounded-full bg-indigo-600 transition-all duration-500"
            style={{
              width: `${job.progress}%`
            }}
          />

        </div>

      </div>


      <div className="mt-6">

        <Link
          href={`/jobs/${job.id}`}
          className="inline-flex rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-slate-800"
        >
          Open Job
        </Link>

      </div>

    </div>
  );
}
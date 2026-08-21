"use client";

import { useEffect, useState } from "react";
import { getJob } from "@/lib/api";
import LiveActivity from "@/components/LiveActivity";

interface Job {
  id: string;
  goal: string;
  status: string;
  progress: number;
  result?: unknown;
  error?: string | null;
}

export default function JobDetailPage({
  params
}: {
  params: Promise<{ id: string }> | { id: string }
}) {
  const [job, setJob] = useState<Job | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);

  useEffect(() => {
    Promise.resolve(params).then((p) => {
      if (p?.id) {
        setJobId(p.id);
      }
    });
  }, [params]);

  useEffect(() => {
    if (!jobId) return;

    let active = true;
    const currentId = jobId;

    async function load() {
      try {
        const data = await getJob(currentId);
        if (active && data) {
          setJob(data as Job);
        }
      } catch (error) {
        console.error(error);
      }
    }

    load();
    const interval = setInterval(load, 2000);
    return () => {
      active = false;
      clearInterval(interval);
    };
  }, [jobId]);

  if (!job) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-50">
        <p className="text-sm text-slate-500">Loading job...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <div className="mx-auto max-w-4xl">
        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <div className="flex items-start justify-between gap-6">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-indigo-600">
                Autonomous Job
              </p>
              <h1 className="mt-2 text-2xl font-semibold text-slate-950">
                {job.goal}
              </h1>
            </div>

            <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
              {job.status}
            </span>
          </div>

          <div className="mt-10">
            <div className="mb-3 flex justify-between">
              <span className="text-sm text-slate-500">Progress</span>
              <span className="text-sm font-semibold text-slate-950">
                {job.progress}%
              </span>
            </div>

            <div className="h-3 overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full bg-indigo-600 transition-all duration-700"
                style={{
                  width: `${job.progress}%`
                }}
              />
            </div>
          </div>

          {job.status === "completed" && (
            <div className="mt-8 rounded-2xl bg-emerald-50 p-5">
              <p className="font-semibold text-emerald-800">Goal completed</p>
              <p className="mt-1 text-sm text-emerald-700">
                Your AI team has finished the job.
              </p>
            </div>
          )}

          {job.status === "failed" && (
            <div className="mt-8 rounded-2xl bg-red-50 p-5">
              <p className="font-semibold text-red-800">Job failed</p>
              <p className="mt-1 text-sm text-red-700">{job.error}</p>
            </div>
          )}
        </div>
      </div>

      {/* Floating Live AI Activity Window */}
      <LiveActivity jobId={jobId || undefined} />
    </main>
  );
}

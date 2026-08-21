"use client";

import { useEffect, useState } from "react";
import { getJob, getJobs } from "@/lib/api";

interface Job {
  id: string;
  goal: string;
  status: string;
  progress: number;
  result?: unknown;
  error?: string | null;
}

export default function JobPage({
  params
}: {
  params?: Promise<{ id?: string }>
}) {
  const [job, setJob] = useState<Job | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [jobId, setJobId] = useState<string | null>(null);

  useEffect(() => {
    if (params) {
      params.then((p) => {
        if (p?.id) setJobId(p.id);
      });
    }
  }, [params]);

  useEffect(() => {
    let active = true;

    async function load() {
      try {
        if (jobId) {
          const data = await getJob(jobId);
          if (active && data) {
            setJob(data as Job);
          }
        } else {
          const data = await getJobs();
          if (active && data) {
            setJobs(data as Job[]);
          }
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

  if (jobId && !job) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-50">
        <p className="text-sm text-slate-500">Loading job...</p>
      </main>
    );
  }

  if (job) {
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
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50 p-6">
      <div className="mx-auto max-w-4xl space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-slate-950">Background Jobs</h1>
            <p className="text-sm text-slate-500">View and track all autonomous AI jobs</p>
          </div>
        </div>

        <div className="space-y-4">
          {jobs.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
              <p className="text-sm text-slate-500">No background jobs found.</p>
            </div>
          ) : (
            jobs.map((j) => (
              <div key={j.id} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-slate-950">{j.goal}</h3>
                  <p className="text-xs text-slate-500 font-mono mt-1">ID: {j.id}</p>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-sm font-semibold text-slate-700">{j.progress}%</span>
                  <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700 capitalize">
                    {j.status}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </main>
  );
}
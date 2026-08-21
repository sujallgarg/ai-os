"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import LiveActivity from "@/components/LiveActivity";
import { getJob } from "@/lib/api";

export default function GoalDetailPage({
  params
}: {
  params: Promise<{ id: string }> | { id: string }
}) {
  const [job, setJob] = useState<any>(null);
  const [goalId, setGoalId] = useState<string | null>(null);

  useEffect(() => {
    Promise.resolve(params).then((p) => {
      if (p?.id) setGoalId(p.id);
    });
  }, [params]);

  useEffect(() => {
    if (!goalId) return;
    async function load() {
      try {
        const data = await getJob(goalId!);
        if (data) setJob(data);
      } catch (e) {
        console.error(e);
      }
    }
    load();
    const interval = setInterval(load, 2000);
    return () => clearInterval(interval);
  }, [goalId]);

  if (!job) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Sidebar />
        <div className="lg:pl-64">
          <Topbar />
          <main className="p-8 text-sm text-slate-500">Loading goal detail...</main>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Topbar />
        <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
            <div className="flex items-start justify-between gap-6">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-indigo-600">Goal Objective</p>
                <h1 className="mt-2 text-2xl font-semibold text-slate-950">{job.goal}</h1>
              </div>
              <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700 capitalize">
                {job.status}
              </span>
            </div>

            <div className="mt-8">
              <div className="mb-2 flex justify-between text-sm">
                <span className="text-slate-500">Execution Progress</span>
                <span className="font-semibold text-slate-950">{job.progress}%</span>
              </div>
              <div className="h-3 overflow-hidden rounded-full bg-slate-100">
                <div
                  className="h-full rounded-full bg-indigo-600 transition-all duration-700"
                  style={{ width: `${job.progress}%` }}
                />
              </div>
            </div>
          </div>
        </main>
      </div>
      <LiveActivity jobId={goalId || undefined} />
    </div>
  );
}

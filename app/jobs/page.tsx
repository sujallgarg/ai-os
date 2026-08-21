"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import GoalCard from "@/components/GoalCard";
import LiveActivity from "@/components/LiveActivity";
import { getJobs } from "@/lib/api";

export default function JobsPage() {
  const [jobs, setJobs] = useState<any[]>([]);

  async function load() {
    try {
      const data = await getJobs();
      setJobs(data || []);
    } catch (e) {
      console.error(e);
    }
  }

  useEffect(() => {
    load();
    const interval = setInterval(load, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Topbar />
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-950">Background Jobs</h1>
            <p className="text-sm text-slate-500 mt-1">Monitor asynchronous batch pipelines and task executions</p>
          </div>

          <div className="space-y-4">
            {jobs.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center text-slate-500 text-sm">
                No active background jobs found.
              </div>
            ) : (
              jobs.map((j) => <GoalCard key={j.id} job={j} />)
            )}
          </div>
        </main>
      </div>
      <LiveActivity />
    </div>
  );
}

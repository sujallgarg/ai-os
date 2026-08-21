"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import LiveActivity from "@/components/LiveActivity";
import { getJobs } from "@/lib/api";

export default function TasksPage() {
  const [jobs, setJobs] = useState<any[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const data = await getJobs();
        setJobs(data || []);
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Topbar />
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-950">Task Graph Management</h1>
            <p className="text-sm text-slate-500 mt-1">Detailed task dependencies, tool calls, and execution steps</p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="font-semibold text-slate-950 mb-4">Active & Queued Tasks</h2>
            <div className="space-y-3">
              {jobs.map((job) => (
                <div key={job.id} className="flex items-center justify-between p-4 rounded-xl border border-slate-100 bg-slate-50">
                  <div>
                    <p className="font-medium text-slate-950">{job.goal}</p>
                    <p className="text-xs text-slate-500 font-mono mt-0.5">Job ID: {job.id}</p>
                  </div>
                  <span className="text-xs font-semibold px-3 py-1 rounded-full bg-indigo-50 text-indigo-700 capitalize">
                    {job.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
      <LiveActivity />
    </div>
  );
}

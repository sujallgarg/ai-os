"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import GoalCard from "@/components/GoalCard";
import LiveActivity from "@/components/LiveActivity";
import { getJobs, createGoal } from "@/lib/api";

export default function GoalsPage() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [goal, setGoal] = useState("");
  const [loading, setLoading] = useState(false);

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

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!goal.trim() || loading) return;
    setLoading(true);
    try {
      const res = await createGoal(goal.trim());
      setGoal("");
      const id = (res as any)?.job_id || (res as any)?.id;
      if (id) {
        window.location.href = `/jobs/${id}`;
      } else {
        await load();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Topbar />
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-950">Autonomous Goals</h1>
            <p className="text-sm text-slate-500 mt-1">Dispatch high-level objectives to your AI team</p>
          </div>

          <form onSubmit={handleSubmit} className="flex gap-3 bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
            <input
              type="text"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="Enter goal (e.g., 'Research 20 SaaS leads and draft outreach emails')..."
              className="flex-1 rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm outline-none focus:border-indigo-400 focus:bg-white"
            />
            <button
              type="submit"
              disabled={loading || !goal.trim()}
              className="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-50"
            >
              {loading ? "Dispatching..." : "Dispatch Goal"}
            </button>
          </form>

          <div className="space-y-4">
            {jobs.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center text-slate-500 text-sm">
                No goals dispatched yet. Use the input above to start.
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

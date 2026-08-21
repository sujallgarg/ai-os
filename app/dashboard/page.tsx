"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import StatCard from "@/components/StatCard";
import GoalCard from "@/components/GoalCard";
import ApprovalCard from "@/components/ApprovalCard";
import { useRealtime } from "@/hooks/useRealtime";

import {
  getAgents,
  getApprovals,
  getJobs,
  createGoal
} from "@/lib/api";

interface Job {
  id: string;
  goal: string;
  status: string;
  progress: number;
  error?: string | null;
}

export default function DashboardPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [agents, setAgents] = useState<any[]>([]);
  const [approvals, setApprovals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const [newGoal, setNewGoal] = useState("");
  const [dispatching, setDispatching] = useState(false);

  const { isConnected } = useRealtime();

  async function loadData() {
    try {
      const [jobsData, agentsData, approvalsData] = await Promise.all([
        getJobs(),
        getAgents(),
        getApprovals()
      ]);
      setJobs(jobsData || []);
      setAgents(agentsData || []);
      setApprovals(approvalsData || []);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 3000);
    return () => clearInterval(interval);
  }, []);

  async function handleDispatchGoal(e: React.FormEvent) {
    e.preventDefault();
    if (!newGoal.trim() || dispatching) return;
    setDispatching(true);
    try {
      const res = await createGoal(newGoal.trim());
      setNewGoal("");
      const targetId = (res as any)?.job_id || (res as any)?.id;
      if (targetId) {
        window.location.href = `/jobs/${targetId}`;
      } else {
        await loadData();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setDispatching(false);
    }
  }

  const activeJobs = jobs.filter((job) => job.status === "running");
  const pendingApprovals = approvals.filter((a) => a.status === "pending" || a.status === "waiting");

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="text-sm text-slate-500">Loading AI workspace...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />

      <div className="lg:pl-64">
        <Topbar />

        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
            <div>
              <p className="text-sm font-medium text-indigo-600">AI Operations</p>
              <h1 className="mt-1 text-3xl font-semibold tracking-tight text-slate-950">
                Your Autonomous AI Team
              </h1>
              <p className="mt-2 text-sm text-slate-500">
                Monitor goals, agents, background jobs, and real-time approvals.
              </p>
            </div>
          </div>

          {/* New Goal Dispatcher Form */}
          <section className="mt-8 rounded-2xl border border-indigo-100 bg-white p-6 shadow-sm">
            <h2 className="text-sm font-semibold uppercase tracking-wider text-indigo-600">
              Dispatch Autonomous Goal
            </h2>
            <form onSubmit={handleDispatchGoal} className="mt-4 flex flex-col gap-3 sm:flex-row">
              <input
                type="text"
                value={newGoal}
                onChange={(e) => setNewGoal(e.target.value)}
                placeholder="Give your AI team a goal (e.g. 'Build a SaaS landing page' or 'Check my Gmail')..."
                className="flex-1 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-indigo-400 focus:bg-white"
              />
              <button
                type="submit"
                disabled={dispatching || !newGoal.trim()}
                className="rounded-xl bg-indigo-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-indigo-700 disabled:opacity-50"
              >
                {dispatching ? "Dispatching..." : "Dispatch Goal"}
              </button>
            </form>
          </section>

          {/* Stats Grid */}
          <section className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard
              label="Active Goals"
              value={activeJobs.length}
              description="Currently executing"
            />
            <StatCard
              label="Total Jobs"
              value={jobs.length}
              description="In task runner queue"
            />
            <StatCard
              label="Agents Online"
              value={agents.length}
              description="Available capabilities"
            />
            <StatCard
              label="Pending Approvals"
              value={pendingApprovals.length}
              description="Requires human gate"
            />
          </section>

          {/* Pending Approvals Section */}
          {pendingApprovals.length > 0 && (
            <section className="mt-8">
              <h2 className="mb-4 text-lg font-semibold text-slate-950">
                Requires Human Authorization
              </h2>
              <div className="grid gap-4 sm:grid-cols-2">
                {pendingApprovals.map((appr) => (
                  <ApprovalCard key={appr.id} approval={appr} onComplete={loadData} />
                ))}
              </div>
            </section>
          )}

          {/* Main Grid */}
          <section className="mt-8 grid gap-6 lg:grid-cols-3">
            {/* Active / Recent Jobs */}
            <div className="lg:col-span-2">
              <div className="mb-4 flex items-center justify-between">
                <h2 className="font-semibold text-slate-950">Active & Recent Jobs</h2>
                <span className="text-sm text-slate-500">{jobs.length} total</span>
              </div>

              <div className="space-y-4">
                {jobs.length === 0 ? (
                  <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
                    <h3 className="font-semibold text-slate-950">No jobs active</h3>
                    <p className="mt-2 text-sm text-slate-500">
                      Give your AI team something to accomplish above.
                    </p>
                  </div>
                ) : (
                  jobs.slice(0, 5).map((job) => <GoalCard key={job.id} job={job} />)
                )}
              </div>
            </div>

            {/* AI Team Roster */}
            <div>
              <h2 className="mb-4 font-semibold text-slate-950">AI Swarm Roster</h2>
              <div className="space-y-3">
                {agents.slice(0, 6).map((agent) => (
                  <div
                    key={agent.name}
                    className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-50 text-xs font-bold text-indigo-600">
                          AI
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-slate-950">{agent.name}</p>
                          <p className="text-xs text-slate-500">
                            {agent.capabilities?.length || 0} capabilities
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center gap-1.5">
                        <span className="h-2 w-2 rounded-full bg-emerald-500" />
                        <span className="text-xs text-slate-500">
                          {agent.status || "Online"}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* Realtime System Status */}
          <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-semibold text-slate-950">Autonomous Infrastructure Status</h2>
                <p className="mt-1 text-sm text-slate-500">
                  Real-time telemetry stream listener active.
                </p>
              </div>

              <div className="flex items-center gap-2 text-sm font-medium text-emerald-600">
                <span className="h-2.5 w-2.5 rounded-full bg-emerald-500 animate-pulse" />
                {isConnected ? "Live Stream Connected" : "Operational"}
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}
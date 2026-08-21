"use client";

import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import LiveActivity from "@/components/LiveActivity";

export default function ActivityPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Topbar />
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-950">Activity Timeline</h1>
            <p className="text-sm text-slate-500 mt-1">Human-readable execution log across all agents and integrations</p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="space-y-4">
              {[
                { time: "Just now", agent: "Email Agent", action: "Connected to Gmail inbox and scanned threads" },
                { time: "5 mins ago", agent: "Planner Agent", action: "Created task DAG for lead generation goal" },
                { time: "12 mins ago", agent: "Browser Agent", action: "Searched web and gathered 20 target profiles" }
              ].map((item, idx) => (
                <div key={idx} className="flex gap-4 items-start border-b border-slate-100 pb-4 last:border-0 last:pb-0">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600 font-bold text-xs">
                    AI
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-slate-950">{item.agent}</p>
                    <p className="text-sm text-slate-600 mt-0.5">{item.action}</p>
                    <p className="text-xs text-slate-400 mt-1">{item.time}</p>
                  </div>
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

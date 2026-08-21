"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import LiveActivity from "@/components/LiveActivity";
import { getAgents } from "@/lib/api";

export default function AgentsPage() {
  const [agents, setAgents] = useState<any[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const data = await getAgents();
        setAgents(data || []);
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
            <h1 className="text-2xl font-bold text-slate-950">AI Agent Roster</h1>
            <p className="text-sm text-slate-500 mt-1">Autonomous agents, capabilities, and system roles</p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {agents.map((agent) => (
              <div key={agent.name} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-50 text-sm font-bold text-indigo-600">
                      AI
                    </div>
                    <span className="flex items-center gap-1.5 text-xs font-medium text-emerald-600">
                      <span className="h-2 w-2 rounded-full bg-emerald-500" />
                      Active
                    </span>
                  </div>

                  <h2 className="mt-4 font-semibold text-slate-950 capitalize">{agent.name} Agent</h2>
                  <p className="mt-1 text-xs text-slate-500">{agent.description || "Specialized autonomous agent"}</p>
                </div>

                <div className="mt-6 border-t border-slate-100 pt-4">
                  <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Capabilities</p>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {agent.capabilities?.map((cap: string) => (
                      <span key={cap} className="rounded-lg bg-slate-100 px-2.5 py-1 text-[11px] font-medium text-slate-700">
                        {cap}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>
      <LiveActivity />
    </div>
  );
}

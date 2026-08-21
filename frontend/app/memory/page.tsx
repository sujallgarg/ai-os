"use client";

import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import LiveActivity from "@/components/LiveActivity";

export default function MemoryPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Topbar />
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-950">Memory Browser</h1>
            <p className="text-sm text-slate-500 mt-1">Cross-session context, persistent user preferences, and agent learnings</p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="font-semibold text-slate-950">Stored Project Context</h2>
            <div className="mt-4 space-y-3">
              <div className="p-4 rounded-xl border border-slate-100 bg-slate-50 flex items-center justify-between">
                <div>
                  <p className="font-medium text-slate-950 text-sm">User Tone & Style Preference</p>
                  <p className="text-xs text-slate-500 mt-0.5">Professional, concise, clear value-first email structure</p>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-indigo-50 text-indigo-700">Active</span>
              </div>
              <div className="p-4 rounded-xl border border-slate-100 bg-slate-50 flex items-center justify-between">
                <div>
                  <p className="font-medium text-slate-950 text-sm">Gmail Integration Scope</p>
                  <p className="text-xs text-slate-500 mt-0.5">Read inbox threads, draft replies, request authorization before send</p>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700">Verified</span>
              </div>
            </div>
          </div>
        </main>
      </div>
      <LiveActivity />
    </div>
  );
}

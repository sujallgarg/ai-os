"use client";

import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import LiveActivity from "@/components/LiveActivity";

export default function SettingsPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Topbar />
        <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-950">Workspace Settings</h1>
            <p className="text-sm text-slate-500 mt-1">Global preferences, policy engines, and platform configuration</p>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm space-y-6">
            <h2 className="font-semibold text-slate-950">System Configuration</h2>
            <div className="space-y-4 text-sm">
              <div className="flex items-center justify-between p-4 rounded-xl border border-slate-100 bg-slate-50">
                <div>
                  <p className="font-medium text-slate-950">Real-time Telemetry Stream</p>
                  <p className="text-xs text-slate-500 mt-0.5">WebSocket connection to `ws://localhost:8000/ws`</p>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700">Active</span>
              </div>
              <div className="flex items-center justify-between p-4 rounded-xl border border-slate-100 bg-slate-50">
                <div>
                  <p className="font-medium text-slate-950">Policy Engine Gate</p>
                  <p className="text-xs text-slate-500 mt-0.5">Enforces human authorization on high-risk tool operations</p>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700">Enforced</span>
              </div>
            </div>
          </div>
        </main>
      </div>
      <LiveActivity />
    </div>
  );
}

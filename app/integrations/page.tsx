"use client";

import Link from "next/link";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import LiveActivity from "@/components/LiveActivity";

export default function IntegrationsPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Topbar />
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-950">Connected Integrations</h1>
            <p className="text-sm text-slate-500 mt-1">Manage external tool capabilities and API connections</p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <Link href="/integrations/gmail" className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:border-indigo-300 transition">
              <div className="flex items-center justify-between">
                <span className="text-xl">📧</span>
                <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700">Connected</span>
              </div>
              <h2 className="mt-4 font-semibold text-slate-950">Gmail</h2>
              <p className="mt-1 text-xs text-slate-500">Read inbox, summarize emails, draft replies, send authorized messages</p>
            </Link>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm opacity-60">
              <div className="flex items-center justify-between">
                <span className="text-xl">🌐</span>
                <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">Available</span>
              </div>
              <h2 className="mt-4 font-semibold text-slate-950">Web Search</h2>
              <p className="mt-1 text-xs text-slate-500">Live internet search and page extraction</p>
            </div>
          </div>
        </main>
      </div>
      <LiveActivity />
    </div>
  );
}

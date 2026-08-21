"use client";

import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import LiveActivity from "@/components/LiveActivity";

export default function GmailIntegrationPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Topbar />
        <main className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-950">Gmail Integration</h1>
            <p className="text-sm text-slate-500 mt-1">Configure OAuth access, scopes, and policy rules for Gmail Agent</p>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm space-y-6">
            <div className="flex items-center justify-between pb-6 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-red-50 text-2xl">
                  📧
                </div>
                <div>
                  <h2 className="font-semibold text-slate-950">Google Workspace / Gmail</h2>
                  <p className="text-xs text-slate-500">OAuth2 Authenticated Scope</p>
                </div>
              </div>
              <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                Connected
              </span>
            </div>

            <div className="space-y-4 text-sm">
              <h3 className="font-semibold text-slate-950">Enforced Security Policies</h3>
              <div className="space-y-2">
                <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <span className="text-slate-700">`gmail.read` & `gmail.search`</span>
                  <span className="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-lg">Allowed Automatically</span>
                </div>
                <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <span className="text-slate-700">`gmail.draft`</span>
                  <span className="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-lg">Allowed Automatically</span>
                </div>
                <div className="flex items-center justify-between p-3 rounded-xl bg-amber-50 border border-amber-100">
                  <span className="text-amber-900 font-medium">`gmail.send` & `gmail.reply`</span>
                  <span className="text-xs font-semibold text-amber-700 bg-white px-2.5 py-1 rounded-lg border border-amber-200">Human Approval Required</span>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
      <LiveActivity />
    </div>
  );
}

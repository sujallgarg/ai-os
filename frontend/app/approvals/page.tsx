"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import ApprovalCard from "@/components/ApprovalCard";
import LiveActivity from "@/components/LiveActivity";
import { getApprovals } from "@/lib/api";

export default function ApprovalsPage() {
  const [approvals, setApprovals] = useState<any[]>([]);

  async function load() {
    try {
      const data = await getApprovals();
      setApprovals(data || []);
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
            <h1 className="text-2xl font-bold text-slate-950">Approval Center</h1>
            <p className="text-sm text-slate-500 mt-1">Human authorization gates for high-risk autonomous actions</p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            {approvals.length === 0 ? (
              <div className="sm:col-span-2 rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center text-slate-500 text-sm">
                No pending approvals. You're all caught up!
              </div>
            ) : (
              approvals.map((appr) => (
                <ApprovalCard key={appr.id} approval={appr} onComplete={load} />
              ))
            )}
          </div>
        </main>
      </div>
      <LiveActivity />
    </div>
  );
}

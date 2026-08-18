"use client";

import React, { useEffect, useState } from "react";
import { AIOSClient } from "@/lib/api";
import { ApprovalRequest } from "@/lib/types";
import { ApprovalCard } from "@/components/approvals/ApprovalCard";
import { Tabs } from "@/components/ui/Tabs";
import { ShieldAlert, ShieldCheck } from "lucide-react";

export default function ApprovalsPage() {
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [activeTab, setActiveTab] = useState("pending");

  const refreshApprovals = () => {
    setApprovals(AIOSClient.getApprovals());
  };

  useEffect(() => {
    refreshApprovals();
    const interval = setInterval(refreshApprovals, 3000);
    return () => clearInterval(interval);
  }, []);

  const pendingList = approvals.filter((a) => a.status === "pending");
  const approvedList = approvals.filter((a) => a.status === "approved");
  const rejectedList = approvals.filter((a) => a.status === "rejected");

  const displayedList =
    activeTab === "pending"
      ? pendingList
      : activeTab === "approved"
      ? approvedList
      : activeTab === "rejected"
      ? rejectedList
      : approvals;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Human Approvals Queue
            </h1>
            {pendingList.length > 0 && (
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-amber-500 text-white animate-pulse">
                {pendingList.length} Pending
              </span>
            )}
          </div>
          <p className="text-xs sm:text-sm text-slate-500 max-w-xl">
            Security policy checkpoint where high-impact tool actions (e.g. outbound emails, git pushes, production commands) require human authorization.
          </p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="border-b border-slate-200/80">
        <Tabs
          tabs={[
            { id: "pending", label: "Pending Review", count: pendingList.length },
            { id: "approved", label: "Approved History", count: approvedList.length },
            { id: "rejected", label: "Denied History", count: rejectedList.length },
            { id: "all", label: "All Tickets", count: approvals.length },
          ]}
          activeTab={activeTab}
          onChange={setActiveTab}
        />
      </div>

      {/* Approvals Grid */}
      {displayedList.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 text-xs text-slate-400 space-y-2">
          <ShieldCheck className="w-8 h-8 text-emerald-500 mx-auto" />
          <p className="font-semibold text-slate-700">No approval tickets in this view.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {displayedList.map((appr) => (
            <ApprovalCard key={appr.id} approval={appr} onHandled={refreshApprovals} />
          ))}
        </div>
      )}
    </div>
  );
}

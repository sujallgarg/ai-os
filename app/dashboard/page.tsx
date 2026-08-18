"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { AIOSClient } from "@/lib/api";
import { Goal, AgentProfile, ApprovalRequest, ActivityEvent, SystemMetrics } from "@/lib/types";
import { MetricCards } from "@/components/dashboard/MetricCards";
import { QuickGoalInput } from "@/components/dashboard/QuickGoalInput";
import { GoalCard } from "@/components/goals/GoalCard";
import { AgentSwarmCard } from "@/components/dashboard/AgentSwarmCard";
import { ApprovalAlertsCard } from "@/components/dashboard/ApprovalAlertsCard";
import { LiveActivityFeed } from "@/components/dashboard/LiveActivityFeed";
import { Button } from "@/components/ui/Button";
import { Target, Plus, ArrowRight, Sparkles, Activity } from "lucide-react";
import { GoalCreationModal } from "@/components/goals/GoalCreationModal";

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<SystemMetrics>(AIOSClient.getMetrics());
  const [goals, setGoals] = useState<Goal[]>([]);
  const [agents, setAgents] = useState<AgentProfile[]>([]);
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [activities, setActivities] = useState<ActivityEvent[]>([]);
  const [isGoalModalOpen, setIsGoalModalOpen] = useState(false);

  const refreshData = () => {
    setMetrics(AIOSClient.getMetrics());
    setGoals(AIOSClient.getGoals());
    setAgents(AIOSClient.getAgents());
    setApprovals(AIOSClient.getApprovals());
    setActivities(AIOSClient.getActivity());
  };

  useEffect(() => {
    refreshData();
    const interval = setInterval(refreshData, 3000);
    return () => clearInterval(interval);
  }, []);

  const activeGoals = goals.filter((g) => g.status === "in_progress" || g.status === "queued");

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Control Center
            </h1>
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
              Autonomous Core Online
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 max-w-xl">
            Autonomous multi-agent operating system coordinating task planning, capability routing, execution DAGs, and security handoffs.
          </p>
        </div>

        <Button
          variant="primary"
          size="md"
          onClick={() => setIsGoalModalOpen(true)}
          leftIcon={<Plus className="w-4 h-4" />}
          className="shadow-sm"
        >
          Dispatch Goal
        </Button>
      </div>

      {/* Metric Cards Grid */}
      <MetricCards metrics={metrics} />

      {/* Hero Quick Goal Dispatcher */}
      <QuickGoalInput />

      {/* Active Autonomous Goals */}
      <div>
        <div className="flex items-center justify-between gap-4 mb-4">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
              <Target className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900 tracking-tight">
                Active Execution DAGs
              </h2>
              <p className="text-xs text-slate-500">Goals currently orchestrated across the Agent Swarm</p>
            </div>
          </div>
          <Link
            href="/goals"
            className="text-xs font-semibold text-primary-600 hover:text-primary-800 flex items-center gap-1 group"
          >
            <span>All Goals ({goals.length})</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
          </Link>
        </div>

        {activeGoals.length === 0 ? (
          <div className="p-8 text-center bg-white rounded-2xl border border-slate-200 text-xs text-slate-400">
            No goals currently in progress. Dispatch a new goal above to begin execution.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {activeGoals.slice(0, 4).map((goal) => (
              <GoalCard key={goal.id} goal={goal} />
            ))}
          </div>
        )}
      </div>

      {/* Two-Column Grid: Agent Swarm + Human Approvals */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AgentSwarmCard agents={agents} />
        <ApprovalAlertsCard approvals={approvals} onApprovalHandled={refreshData} />
      </div>

      {/* Live System Telemetry Stream */}
      <LiveActivityFeed activities={activities} />

      {/* Modal */}
      <GoalCreationModal
        isOpen={isGoalModalOpen}
        onClose={() => {
          setIsGoalModalOpen(false);
          refreshData();
        }}
      />
    </div>
  );
}

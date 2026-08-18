"use client";

import React from "react";
import { SystemMetrics } from "@/lib/types";
import { Stat } from "@/components/ui/Stat";
import { Target, CheckCircle2, Bot, ShieldAlert, Cpu, Database } from "lucide-react";

export interface MetricCardsProps {
  metrics: SystemMetrics;
}

export function MetricCards({ metrics }: MetricCardsProps) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
      <Stat
        label="Active Goals"
        value={metrics.activeGoals}
        description="Autonomous DAGs"
        change="+2 today"
        changeType="positive"
        icon={<Target className="w-4 h-4 text-blue-600" />}
      />
      <Stat
        label="Completed Goals"
        value={metrics.totalGoalsCompleted}
        description="100% finished"
        change="98% success"
        changeType="positive"
        icon={<CheckCircle2 className="w-4 h-4 text-emerald-600" />}
      />
      <Stat
        label="Agent Swarm"
        value={`${metrics.activeAgents}/${metrics.totalAgents}`}
        description="Ready for dispatch"
        change="6 Online"
        changeType="positive"
        icon={<Bot className="w-4 h-4 text-violet-600" />}
      />
      <Stat
        label="Pending Approvals"
        value={metrics.pendingApprovals}
        description="Human-in-the-loop"
        change={metrics.pendingApprovals > 0 ? "Action required" : "Clear"}
        changeType={metrics.pendingApprovals > 0 ? "negative" : "positive"}
        icon={<ShieldAlert className="w-4 h-4 text-amber-600" />}
      />
      <Stat
        label="Tasks Executed"
        value={metrics.totalTasksExecuted}
        description="Avg 1.42s latency"
        icon={<Cpu className="w-4 h-4 text-primary-600" />}
      />
      <Stat
        label="Shared Memory"
        value={metrics.memoryItemsCount}
        description="Persistent knowledge"
        icon={<Database className="w-4 h-4 text-slate-600" />}
      />
    </div>
  );
}

"use client";

import React from "react";
import Link from "next/link";
import { ActivityEvent } from "@/lib/types";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { formatRelativeTime, cn } from "@/lib/utils";
import { Activity, ArrowRight, CheckCircle2, AlertTriangle, ShieldCheck, Play, Database, RefreshCw } from "lucide-react";

export interface LiveActivityFeedProps {
  activities: ActivityEvent[];
}

export function LiveActivityFeed({ activities }: LiveActivityFeedProps) {
  const getEventIcon = (type: ActivityEvent["event_type"], severity: ActivityEvent["severity"]) => {
    switch (type) {
      case "task_completed":
        return <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />;
      case "approval_required":
        return <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />;
      case "approval_granted":
        return <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />;
      case "task_started":
        return <Play className="w-3.5 h-3.5 text-blue-600" />;
      case "memory_write":
        return <Database className="w-3.5 h-3.5 text-indigo-600" />;
      case "replan":
        return <RefreshCw className="w-3.5 h-3.5 text-purple-600" />;
      default:
        return <Activity className="w-3.5 h-3.5 text-slate-500" />;
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl bg-slate-50 text-slate-700 flex items-center justify-center">
            <Activity className="w-4 h-4" />
          </div>
          <div>
            <CardTitle>Live System Telemetry & Event Stream</CardTitle>
            <CardDescription>Real-time execution log across all agents</CardDescription>
          </div>
        </div>
        <Link
          href="/activity"
          className="text-xs font-semibold text-primary-600 hover:text-primary-800 flex items-center gap-1 group"
        >
          <span>Full stream</span>
          <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
        </Link>
      </CardHeader>

      <div className="space-y-2.5">
        {activities.slice(0, 5).map((act) => (
          <div
            key={act.id}
            className="flex items-start gap-3 p-2.5 rounded-xl hover:bg-slate-50 transition-colors"
          >
            <div className="w-7 h-7 rounded-lg bg-slate-100/80 border border-slate-200/60 flex items-center justify-center flex-shrink-0 mt-0.5">
              {getEventIcon(act.event_type, act.severity)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs font-semibold text-slate-900 truncate">
                  {act.title}
                </span>
                <span className="text-[10px] text-slate-400 font-mono flex-shrink-0">
                  {formatRelativeTime(act.timestamp)}
                </span>
              </div>
              <p className="text-[11px] text-slate-500 line-clamp-1 mt-0.5">
                {act.description}
              </p>
              {act.agent_name && (
                <span className="text-[10px] font-medium text-slate-400 mt-1 inline-block">
                  Agent: <strong className="text-slate-600 font-semibold">{act.agent_name}</strong>
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

"use client";

import React from "react";
import Link from "next/link";
import { Goal } from "@/lib/types";
import { getGoalStatusBadge, formatRelativeTime, cn } from "@/lib/utils";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { ArrowRight, CheckCircle2, Clock, AlertTriangle, Layers } from "lucide-react";

export interface GoalCardProps {
  goal: Goal;
}

export function GoalCard({ goal }: GoalCardProps) {
  const statusBadge = getGoalStatusBadge(goal.status);

  return (
    <Link
      href={`/goals/${goal.id}`}
      className="block group bg-white border border-slate-200/80 hover:border-primary-300/80 rounded-2xl p-5 shadow-card hover:shadow-elevated transition-all duration-200 select-none"
    >
      <div className="flex items-start justify-between gap-4 mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1.5 flex-wrap">
            <span className="text-[11px] font-mono font-bold text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded">
              {goal.id}
            </span>
            <span
              className={cn(
                "text-xs px-2.5 py-0.5 rounded-full font-semibold border inline-flex items-center gap-1.5",
                statusBadge.className
              )}
            >
              <span className={cn("w-1.5 h-1.5 rounded-full", statusBadge.dotClass)} />
              {statusBadge.label}
            </span>
            <span className="text-xs text-slate-400">
              {formatRelativeTime(goal.created_at)}
            </span>
          </div>
          <h3 className="text-base font-semibold text-slate-900 group-hover:text-primary-700 transition-colors tracking-tight line-clamp-1">
            {goal.title}
          </h3>
        </div>
        <div className="w-8 h-8 rounded-xl bg-slate-50 group-hover:bg-primary-50 text-slate-400 group-hover:text-primary-600 flex items-center justify-center transition-colors flex-shrink-0">
          <ArrowRight className="w-4 h-4" />
        </div>
      </div>

      <p className="text-xs text-slate-500 line-clamp-2 mb-4 leading-relaxed">
        {goal.description}
      </p>

      {/* Progress Bar */}
      <div className="space-y-1.5 mb-4">
        <div className="flex items-center justify-between text-xs">
          <span className="text-slate-500 font-medium flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-slate-400" />
            <span>
              {goal.completed_tasks} of {goal.total_tasks} tasks complete
            </span>
          </span>
          <span className="font-bold text-slate-800 font-mono">
            {goal.progress}%
          </span>
        </div>
        <ProgressBar
          value={goal.progress}
          color={
            goal.status === "completed"
              ? "emerald"
              : goal.status === "partial_failure"
              ? "amber"
              : "primary"
          }
          size="sm"
        />
      </div>

      {/* Tags and Agent Assignments */}
      <div className="flex items-center justify-between pt-3 border-t border-slate-100 flex-wrap gap-2">
        <div className="flex flex-wrap gap-1.5">
          {goal.tags.map((tag) => (
            <span
              key={tag}
              className="text-[10px] font-medium text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md"
            >
              #{tag}
            </span>
          ))}
        </div>
        {goal.supervisor_decision && (
          <span className="text-[11px] font-medium text-slate-400 italic truncate max-w-[200px]">
            Supervisor: {goal.supervisor_decision.action}
          </span>
        )}
      </div>
    </Link>
  );
}

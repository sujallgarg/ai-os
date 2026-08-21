"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { AIOSClient } from "@/lib/api";
import { Goal } from "@/lib/types";
import { TaskGraphVisualizer } from "@/components/goals/TaskGraphVisualizer";
import { SupervisorDecisionFeed } from "@/components/goals/SupervisorDecisionFeed";
import { ArtifactsViewer } from "@/components/goals/ArtifactsViewer";
import { TaskTable } from "@/components/tasks/TaskTable";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Button } from "@/components/ui/Button";
import { getGoalStatusBadge, formatRelativeTime, cn } from "@/lib/utils";
import {
  ArrowLeft,
  Target,
  Layers,
  FileCode,
  ShieldAlert,
  RotateCcw,
  CheckCircle2,
  Calendar
} from "lucide-react";

export default function GoalDetailPage() {
  const params = useParams();
  const router = useRouter();
  const goalId = params.id as string;

  const [goal, setGoal] = useState<Goal | null>(null);

  const fetchGoal = () => {
    const found = AIOSClient.getGoal(goalId);
    if (found) setGoal(found);
  };

  useEffect(() => {
    fetchGoal();
    const interval = setInterval(fetchGoal, 2500);
    return () => clearInterval(interval);
  }, [goalId]);

  if (!goal) {
    return (
      <div className="py-16 text-center space-y-3">
        <p className="text-sm text-slate-500">Loading autonomous goal execution plan...</p>
        <Link href="/goals" className="text-xs text-primary-600 font-semibold hover:underline">
          Return to Goals
        </Link>
      </div>
    );
  }

  const statusBadge = getGoalStatusBadge(goal.status);

  return (
    <div className="space-y-6">
      {/* Top Navigation & Breadcrumbs */}
      <div className="flex items-center justify-between gap-4">
        <Link
          href="/goals"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Goals</span>
        </Link>

        <div className="flex items-center gap-2">
          <Button
            size="sm"
            variant="outline"
            onClick={() => {
              if (confirm("Reset this goal to restart execution?")) {
                const updated = AIOSClient.getGoals().find((g) => g.id === goal.id);
                if (updated) {
                  updated.tasks.forEach((t) => {
                    t.status = t.depends_on.length === 0 ? "ready" : "pending";
                  });
                  updated.status = "in_progress";
                  updated.progress = 0;
                  updated.completed_tasks = 0;
                  setGoal({ ...updated });
                }
              }
            }}
            leftIcon={<RotateCcw className="w-3.5 h-3.5" />}
          >
            Restart Plan
          </Button>
        </div>
      </div>

      {/* Goal Header Hero Card */}
      <div className="bg-white border border-slate-200/90 rounded-3xl p-6 sm:p-8 shadow-card space-y-5">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div className="space-y-2 flex-1 min-w-[300px]">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-xs font-mono font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
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
              <span className="text-xs text-slate-400 font-mono">
                Dispatched {formatRelativeTime(goal.created_at)}
              </span>
            </div>

            <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
              {goal.title}
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              {goal.description}
            </p>
          </div>

          {/* Execution Progress Summary */}
          <div className="bg-slate-50 border border-slate-100 rounded-2xl p-4 min-w-[220px] text-right">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
              Overall Progress
            </span>
            <span className="text-3xl font-extrabold text-slate-900 font-mono">
              {goal.progress}%
            </span>
            <span className="text-xs text-slate-500 block mt-1">
              {goal.completed_tasks} of {goal.total_tasks} Tasks Complete
            </span>
          </div>
        </div>

        {/* Progress Bar */}
        <ProgressBar
          value={goal.progress}
          color={goal.status === "completed" ? "emerald" : "primary"}
          size="md"
        />

        {/* Metadata Footer */}
        <div className="flex items-center justify-between pt-4 border-t border-slate-100 text-xs text-slate-500 flex-wrap gap-2">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-400">Tags:</span>
            {goal.tags.map((tag) => (
              <span
                key={tag}
                className="text-[11px] font-medium text-slate-600 bg-slate-100 px-2 py-0.5 rounded-md"
              >
                #{tag}
              </span>
            ))}
          </div>
          <span className="font-mono text-slate-400 text-[11px]">
            Supervisor ID: sup-core-01
          </span>
        </div>
      </div>

      {/* Supervisor Telemetry Feed */}
      {goal.supervisor_decision && (
        <SupervisorDecisionFeed decision={goal.supervisor_decision} />
      )}

      {/* Interactive DAG Task Graph Visualizer */}
      <div>
        <div className="flex items-center gap-2 mb-3">
          <Layers className="w-4 h-4 text-primary-600" />
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
            Visual Execution DAG
          </h2>
        </div>
        <TaskGraphVisualizer goal={goal} onGoalUpdated={(g) => setGoal({ ...g })} />
      </div>

      {/* Generated Artifacts & Assets */}
      <div>
        <div className="flex items-center gap-2 mb-3">
          <FileCode className="w-4 h-4 text-violet-600" />
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
            Output Artifacts & Deliverables ({goal.artifacts?.length || 0})
          </h2>
        </div>
        <ArtifactsViewer artifacts={goal.artifacts} />
      </div>

      {/* Tasks Table */}
      <div>
        <div className="flex items-center gap-2 mb-3">
          <Target className="w-4 h-4 text-indigo-600" />
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
            Goal Task Queue Details
          </h2>
        </div>
        <TaskTable tasks={goal.tasks} onTaskUpdated={fetchGoal} />
      </div>
    </div>
  );
}

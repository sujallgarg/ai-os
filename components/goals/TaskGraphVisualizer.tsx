"use client";

import React, { useState } from "react";
import { ExecutionTask, Goal } from "@/lib/types";
import { calculateTaskGraphLevels, getAgentColor, getTaskStatusBadge, formatDuration, cn } from "@/lib/utils";
import {
  CheckCircle2,
  Clock,
  Play,
  RotateCw,
  ShieldAlert,
  AlertCircle,
  ArrowRight,
  Terminal,
  Cpu,
  Layers,
  ChevronRight,
  Sliders
} from "lucide-react";
import { Drawer } from "@/components/ui/Drawer";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { AIOSClient } from "@/lib/api";

export interface TaskGraphVisualizerProps {
  goal: Goal;
  onGoalUpdated?: (updated: Goal) => void;
}

export function TaskGraphVisualizer({ goal, onGoalUpdated }: TaskGraphVisualizerProps) {
  const [selectedTask, setSelectedTask] = useState<ExecutionTask | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const levels = calculateTaskGraphLevels(goal.tasks);

  const getStatusIcon = (status: ExecutionTask["status"]) => {
    switch (status) {
      case "completed":
        return <CheckCircle2 className="w-4 h-4 text-emerald-600" />;
      case "running":
        return <RotateCw className="w-4 h-4 text-blue-600 animate-spin" />;
      case "waiting_approval":
        return <ShieldAlert className="w-4 h-4 text-amber-600 animate-pulse" />;
      case "ready":
        return <Play className="w-4 h-4 text-indigo-600" />;
      case "failed":
        return <AlertCircle className="w-4 h-4 text-red-600" />;
      case "pending":
      default:
        return <Clock className="w-4 h-4 text-slate-400" />;
    }
  };

  const handleStepSimulation = () => {
    setIsSimulating(true);

    // Find the first running, ready, or pending task to advance
    const currentRunning = goal.tasks.find((t) => t.status === "running");
    const nextReady = goal.tasks.find((t) => t.status === "ready");
    const nextPending = goal.tasks.find((t) => t.status === "pending");

    if (currentRunning) {
      const updatedGoal = AIOSClient.updateGoalTask(goal.id, currentRunning.id, {
        status: "completed",
        completed_at: new Date().toISOString(),
        duration_ms: Math.floor(Math.random() * 1500) + 800,
        output: { result: "Success", timestamp: new Date().toISOString() }
      });

      // Also unlock downstream tasks whose dependencies are now fulfilled
      if (updatedGoal) {
        updatedGoal.tasks.forEach((t) => {
          if (t.status === "pending" && t.depends_on.every((dId) => {
            const depTask = updatedGoal.tasks.find((dt) => dt.id === dId);
            return depTask?.status === "completed";
          })) {
            AIOSClient.updateGoalTask(goal.id, t.id, { status: "ready" });
          }
        });
      }

      if (updatedGoal && onGoalUpdated) onGoalUpdated(updatedGoal);
    } else if (nextReady) {
      const updatedGoal = AIOSClient.updateGoalTask(goal.id, nextReady.id, {
        status: "running",
        started_at: new Date().toISOString()
      });
      if (updatedGoal && onGoalUpdated) onGoalUpdated(updatedGoal);
    } else if (nextPending) {
      const updatedGoal = AIOSClient.updateGoalTask(goal.id, nextPending.id, {
        status: "ready"
      });
      if (updatedGoal && onGoalUpdated) onGoalUpdated(updatedGoal);
    }

    setTimeout(() => {
      setIsSimulating(false);
    }, 400);
  };

  return (
    <div className="space-y-4">
      {/* Workflow Stage Pipeline Breadcrumb */}
      <div className="bg-slate-50 border border-slate-200/80 rounded-2xl p-4">
        <div className="flex items-center justify-between flex-wrap gap-3 mb-3">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-primary-600" />
            <span className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Autonomous Execution DAG Pipeline
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={handleStepSimulation}
              isLoading={isSimulating}
              leftIcon={<Play className="w-3.5 h-3.5 text-primary-600" />}
              className="bg-white"
            >
              Simulate Execution Step
            </Button>
          </div>
        </div>

        {/* Pipeline Progression Steps */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-1.5 text-center text-[11px] select-none">
          {[
            { label: "1. User Goal", active: true, done: true },
            { label: "2. Planner", active: true, done: true },
            { label: "3. Task Graph", active: true, done: true },
            { label: "4. Matcher", active: true, done: true },
            { label: "5. Supervisor", active: true, done: goal.progress > 0 },
            { label: "6. Executor", active: goal.status === "in_progress", done: goal.progress === 100 },
            { label: "7. Completion", active: goal.status === "completed", done: goal.status === "completed" },
          ].map((step, idx) => (
            <div
              key={idx}
              className={cn(
                "py-1.5 px-2 rounded-lg border font-medium transition-colors",
                step.done
                  ? "bg-emerald-50 text-emerald-800 border-emerald-200"
                  : step.active
                  ? "bg-primary-50 text-primary-800 border-primary-200 font-semibold"
                  : "bg-white text-slate-400 border-slate-200"
              )}
            >
              {step.label}
            </div>
          ))}
        </div>
      </div>

      {/* Visual DAG Nodes Across Topological Columns */}
      <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-card overflow-x-auto">
        <div className="flex items-stretch gap-6 min-w-[700px]">
          {levels.map((columnTasks, colIdx) => (
            <React.Fragment key={colIdx}>
              {/* Column */}
              <div className="flex-1 flex flex-col gap-4">
                <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                    Stage {colIdx + 1}
                  </span>
                  <span className="text-[11px] font-mono text-slate-400 bg-slate-50 px-1.5 py-0.5 rounded border border-slate-100">
                    {columnTasks.length} {columnTasks.length === 1 ? "task" : "tasks"}
                  </span>
                </div>

                <div className="flex flex-col gap-3 flex-1 justify-around">
                  {columnTasks.map((task) => {
                    const statusBadge = getTaskStatusBadge(task.status);
                    const agentColor = getAgentColor(task.agent);
                    const isSelected = selectedTask?.id === task.id;

                    return (
                      <div
                        key={task.id}
                        onClick={() => setSelectedTask(task)}
                        className={cn(
                          "group relative bg-white border rounded-2xl p-4 shadow-subtle hover:shadow-card cursor-pointer transition-all duration-150 select-none",
                          isSelected
                            ? "border-primary-500 ring-2 ring-primary-500/10 shadow-elevated"
                            : task.status === "running"
                            ? "border-blue-400 ring-2 ring-blue-500/10 bg-blue-50/10"
                            : "border-slate-200/90 hover:border-slate-300"
                        )}
                      >
                        {/* Task Top Bar */}
                        <div className="flex items-center justify-between gap-2 mb-2">
                          <div className="flex items-center gap-1.5">
                            <span className="text-[11px] font-mono font-bold text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded">
                              #{task.id}
                            </span>
                            <span className={cn("text-[11px] px-2 py-0.5 rounded-md font-semibold border flex items-center gap-1", statusBadge.className)}>
                              {getStatusIcon(task.status)}
                              {statusBadge.label}
                            </span>
                          </div>
                          {task.duration_ms && (
                            <span className="text-[10px] font-mono text-slate-400">
                              {formatDuration(task.duration_ms)}
                            </span>
                          )}
                        </div>

                        {/* Description */}
                        <p className="text-xs font-semibold text-slate-900 leading-snug mb-3 line-clamp-2">
                          {task.description}
                        </p>

                        {/* Agent & Capability Tags */}
                        <div className="flex flex-wrap items-center gap-1.5 pt-2 border-t border-slate-100">
                          {task.agent && (
                            <span className={cn("text-[10px] font-bold px-2 py-0.5 rounded-full border", agentColor.pill, agentColor.border)}>
                              {task.agent}
                            </span>
                          )}
                          {task.tool_name && (
                            <span className="text-[10px] font-mono text-slate-500 bg-slate-50 px-1.5 py-0.5 rounded border border-slate-100">
                              {task.tool_name}
                            </span>
                          )}
                        </div>

                        {/* Dependencies pill */}
                        {task.depends_on.length > 0 && (
                          <div className="mt-2 text-[10px] text-slate-400 flex items-center gap-1">
                            <span>Requires:</span>
                            {task.depends_on.map((d) => (
                              <span key={d} className="font-mono bg-slate-100 px-1 rounded text-slate-600">
                                #{d}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Arrow Connector Between Stages */}
              {colIdx < levels.length - 1 && (
                <div className="flex items-center justify-center text-slate-300">
                  <ChevronRight className="w-5 h-5" />
                </div>
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* Task Inspection Drawer */}
      <Drawer
        isOpen={!!selectedTask}
        onClose={() => setSelectedTask(null)}
        width="lg"
        title={
          selectedTask && (
            <div className="flex items-center gap-2">
              <span className="font-mono font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded text-xs">
                Task #{selectedTask.id}
              </span>
              <span>Task Execution Details</span>
            </div>
          )
        }
        description={selectedTask?.description}
        footer={
          selectedTask && (
            <div className="flex items-center justify-between w-full">
              <span className="text-xs text-slate-400">
                Priority: <strong className="text-slate-700">{selectedTask.priority} / 10</strong>
              </span>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    if (!selectedTask) return;
                    AIOSClient.updateGoalTask(goal.id, selectedTask.id, {
                      status: "running",
                      started_at: new Date().toISOString()
                    });
                    setSelectedTask(null);
                  }}
                >
                  Force Execute
                </Button>
                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => {
                    if (!selectedTask) return;
                    AIOSClient.updateGoalTask(goal.id, selectedTask.id, {
                      status: "completed",
                      completed_at: new Date().toISOString(),
                      duration_ms: 1200
                    });
                    setSelectedTask(null);
                  }}
                >
                  Mark Completed
                </Button>
              </div>
            </div>
          )
        }
      >
        {selectedTask && (
          <div className="space-y-5">
            {/* Status overview */}
            <div className="grid grid-cols-2 gap-3 p-4 bg-slate-50 rounded-2xl border border-slate-100">
              <div>
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                  Status
                </span>
                <Badge variant={selectedTask.status === "completed" ? "success" : selectedTask.status === "running" ? "primary" : "neutral"}>
                  {selectedTask.status}
                </Badge>
              </div>
              <div>
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                  Assigned Agent
                </span>
                <span className="text-xs font-bold text-slate-800 capitalize">
                  {selectedTask.agent || "Unassigned"}
                </span>
              </div>
              <div>
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                  Action Method
                </span>
                <span className="text-xs font-mono text-slate-700">
                  {selectedTask.action}
                </span>
              </div>
              <div>
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                  Tool Hook
                </span>
                <span className="text-xs font-mono text-slate-700">
                  {selectedTask.tool_name || "Internal"}
                </span>
              </div>
            </div>

            {/* Required Capabilities */}
            <div>
              <span className="text-xs font-bold text-slate-800 block mb-2">
                Required Agent Capabilities
              </span>
              <div className="flex flex-wrap gap-1.5">
                {selectedTask.required_capabilities.map((cap) => (
                  <span
                    key={cap}
                    className="text-xs font-mono bg-slate-100 text-slate-700 px-2.5 py-1 rounded-lg border border-slate-200"
                  >
                    {cap}
                  </span>
                ))}
              </div>
            </div>

            {/* Parameters Payload */}
            <div>
              <span className="text-xs font-bold text-slate-800 block mb-2">
                Task Parameters
              </span>
              <pre className="text-xs font-mono bg-slate-900 text-slate-100 p-4 rounded-2xl overflow-x-auto">
                {JSON.stringify(selectedTask.parameters, null, 2)}
              </pre>
            </div>

            {/* Execution Output */}
            {selectedTask.output && (
              <div>
                <span className="text-xs font-bold text-slate-800 block mb-2">
                  Execution Output Payload
                </span>
                <pre className="text-xs font-mono bg-slate-50 text-slate-800 border border-slate-200 p-4 rounded-2xl overflow-x-auto">
                  {JSON.stringify(selectedTask.output, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}
      </Drawer>
    </div>
  );
}

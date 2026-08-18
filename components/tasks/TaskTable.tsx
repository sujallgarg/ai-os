"use client";

import React, { useState } from "react";
import { ExecutionTask } from "@/lib/types";
import { getTaskStatusBadge, getAgentColor, formatDuration, cn } from "@/lib/utils";
import { Drawer } from "@/components/ui/Drawer";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { CheckCircle2, RotateCw, Play, ShieldAlert, AlertCircle, Clock, Search, Filter } from "lucide-react";
import { AIOSClient } from "@/lib/api";

export interface TaskTableProps {
  tasks: ExecutionTask[];
  onTaskUpdated?: () => void;
}

export function TaskTable({ tasks, onTaskUpdated }: TaskTableProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [selectedTask, setSelectedTask] = useState<ExecutionTask | null>(null);

  const filteredTasks = tasks.filter((t) => {
    const matchesSearch =
      t.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (t.agent && t.agent.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (t.tool_name && t.tool_name.toLowerCase().includes(searchQuery.toLowerCase()));

    const matchesStatus = statusFilter === "all" || t.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const getStatusIcon = (status: ExecutionTask["status"]) => {
    switch (status) {
      case "completed":
        return <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />;
      case "running":
        return <RotateCw className="w-3.5 h-3.5 text-blue-600 animate-spin" />;
      case "waiting_approval":
        return <ShieldAlert className="w-3.5 h-3.5 text-amber-600 animate-pulse" />;
      case "ready":
        return <Play className="w-3.5 h-3.5 text-indigo-600" />;
      case "failed":
        return <AlertCircle className="w-3.5 h-3.5 text-red-600" />;
      default:
        return <Clock className="w-3.5 h-3.5 text-slate-400" />;
    }
  };

  return (
    <div className="space-y-4">
      {/* Search & Filter Bar */}
      <div className="flex items-center justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-2 flex-1 max-w-sm">
          <div className="relative w-full">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Filter tasks by description, agent, tool..."
              className="w-full bg-white border border-slate-200 rounded-xl pl-9 pr-3.5 py-2 text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-500/10"
            />
          </div>
        </div>

        <div className="flex items-center gap-1.5 flex-wrap">
          {["all", "ready", "running", "waiting_approval", "completed", "failed"].map((status) => (
            <button
              key={status}
              onClick={() => setStatusFilter(status)}
              className={cn(
                "px-2.5 py-1 text-xs font-semibold rounded-lg capitalize transition-colors",
                statusFilter === status
                  ? "bg-slate-900 text-white"
                  : "bg-white text-slate-600 hover:bg-slate-100 border border-slate-200"
              )}
            >
              {status.replace("_", " ")}
            </button>
          ))}
        </div>
      </div>

      {/* Table Container */}
      <div className="bg-white border border-slate-200/90 rounded-2xl shadow-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50/80 border-b border-slate-200/80 text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
              <tr>
                <th className="px-4 py-3">Task ID</th>
                <th className="px-4 py-3">Description</th>
                <th className="px-4 py-3">Assigned Agent</th>
                <th className="px-4 py-3">Tool Hook</th>
                <th className="px-4 py-3">Priority</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3 text-right">Duration</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium">
              {filteredTasks.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-8 text-center text-slate-400 text-xs">
                    No matching tasks found.
                  </td>
                </tr>
              ) : (
                filteredTasks.map((task) => {
                  const statusBadge = getTaskStatusBadge(task.status);
                  const agentColor = getAgentColor(task.agent);

                  return (
                    <tr
                      key={task.id}
                      onClick={() => setSelectedTask(task)}
                      className="hover:bg-slate-50/70 cursor-pointer transition-colors"
                    >
                      <td className="px-4 py-3 font-mono font-bold text-slate-400">
                        #{task.id}
                      </td>
                      <td className="px-4 py-3 max-w-xs truncate font-semibold text-slate-900">
                        {task.description}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        {task.agent ? (
                          <span
                            className={cn(
                              "text-[10px] font-bold px-2 py-0.5 rounded-full border",
                              agentColor.pill,
                              agentColor.border
                            )}
                          >
                            {task.agent}
                          </span>
                        ) : (
                          <span className="text-slate-400 italic">Unassigned</span>
                        )}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap font-mono text-[11px] text-slate-500">
                        {task.tool_name || "—"}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className="font-bold text-slate-800">{task.priority}</span>
                        <span className="text-slate-400 text-[10px]"> / 10</span>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span
                          className={cn(
                            "text-[11px] px-2 py-0.5 rounded-md font-semibold border inline-flex items-center gap-1.5",
                            statusBadge.className
                          )}
                        >
                          {getStatusIcon(task.status)}
                          {statusBadge.label}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right whitespace-nowrap font-mono text-slate-400">
                        {formatDuration(task.duration_ms)}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Task Detail Drawer */}
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
              <span>Task Execution Profile</span>
            </div>
          )
        }
        description={selectedTask?.description}
      >
        {selectedTask && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3 p-4 bg-slate-50 rounded-2xl border border-slate-100 text-xs">
              <div>
                <span className="text-slate-400 block mb-0.5">Assigned Agent</span>
                <strong className="text-slate-800">{selectedTask.agent || "Unassigned"}</strong>
              </div>
              <div>
                <span className="text-slate-400 block mb-0.5">Tool Action</span>
                <strong className="text-slate-800 font-mono">{selectedTask.action}</strong>
              </div>
              <div>
                <span className="text-slate-400 block mb-0.5">Priority Weight</span>
                <strong className="text-slate-800">{selectedTask.priority} / 10</strong>
              </div>
              <div>
                <span className="text-slate-400 block mb-0.5">Status</span>
                <strong className="text-slate-800 capitalize">{selectedTask.status}</strong>
              </div>
            </div>

            <div>
              <span className="text-xs font-bold text-slate-800 block mb-1.5">
                Parameters
              </span>
              <pre className="text-xs font-mono bg-slate-900 text-slate-100 p-4 rounded-xl overflow-x-auto">
                {JSON.stringify(selectedTask.parameters, null, 2)}
              </pre>
            </div>

            {selectedTask.output && (
              <div>
                <span className="text-xs font-bold text-slate-800 block mb-1.5">
                  Output Data
                </span>
                <pre className="text-xs font-mono bg-slate-50 text-slate-800 border border-slate-200 p-4 rounded-xl overflow-x-auto">
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

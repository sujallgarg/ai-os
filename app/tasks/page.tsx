"use client";

import React, { useEffect, useState } from "react";
import { AIOSClient } from "@/lib/api";
import { ExecutionTask } from "@/lib/types";
import { TaskTable } from "@/components/tasks/TaskTable";
import { CheckSquare } from "lucide-react";

export default function TasksPage() {
  const [tasks, setTasks] = useState<ExecutionTask[]>([]);

  const fetchTasks = () => {
    const goals = AIOSClient.getGoals();
    const allTasks = goals.flatMap((g) => g.tasks);
    setTasks(allTasks);
  };

  useEffect(() => {
    fetchTasks();
    const interval = setInterval(fetchTasks, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Task Execution Queue
          </h1>
          <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
            {tasks.length} Total Tasks
          </span>
        </div>
        <p className="text-xs sm:text-sm text-slate-500 max-w-xl">
          Unified execution queue across all active and completed autonomous goals, prioritized by dependency order and urgency.
        </p>
      </div>

      {/* Table */}
      <TaskTable tasks={tasks} onTaskUpdated={fetchTasks} />
    </div>
  );
}

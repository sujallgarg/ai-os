import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { ExecutionTask, GoalStatusType, TaskStatusType, ApprovalStatusType, RiskLevel, MemoryType } from "./types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateString?: string | null): string {
  if (!dateString) return "—";
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString;
    return new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    }).format(date);
  } catch {
    return dateString;
  }
}

export function formatRelativeTime(dateString?: string | null): string {
  if (!dateString) return "—";
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString;
    const now = new Date();
    const diffSec = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (diffSec < 10) return "just now";
    if (diffSec < 60) return `${diffSec}s ago`;
    const diffMin = Math.floor(diffSec / 60);
    if (diffMin < 60) return `${diffMin}m ago`;
    const diffHr = Math.floor(diffMin / 60);
    if (diffHr < 24) return `${diffHr}h ago`;
    const diffDays = Math.floor(diffHr / 24);
    if (diffDays < 7) return `${diffDays}d ago`;
    return formatDate(dateString);
  } catch {
    return dateString;
  }
}

export function formatDuration(ms?: number): string {
  if (!ms || ms <= 0) return "—";
  if (ms < 1000) return `${ms}ms`;
  const sec = (ms / 1000).toFixed(1);
  if (parseFloat(sec) < 60) return `${sec}s`;
  const min = Math.floor(ms / 60000);
  const remSec = Math.floor((ms % 60000) / 1000);
  return `${min}m ${remSec}s`;
}

export function getGoalStatusBadge(status: GoalStatusType): {
  label: string;
  className: string;
  dotClass: string;
} {
  switch (status) {
    case "completed":
      return {
        label: "Completed",
        className: "bg-emerald-50 text-emerald-700 border-emerald-200/80",
        dotClass: "bg-emerald-500",
      };
    case "in_progress":
      return {
        label: "In Progress",
        className: "bg-blue-50 text-blue-700 border-blue-200/80",
        dotClass: "bg-blue-500 animate-pulse",
      };
    case "partial_failure":
      return {
        label: "Partial Failure",
        className: "bg-amber-50 text-amber-800 border-amber-200/80",
        dotClass: "bg-amber-500",
      };
    case "failed":
      return {
        label: "Failed",
        className: "bg-red-50 text-red-700 border-red-200/80",
        dotClass: "bg-red-500",
      };
    case "paused":
      return {
        label: "Paused",
        className: "bg-slate-100 text-slate-700 border-slate-200",
        dotClass: "bg-slate-400",
      };
    case "queued":
    default:
      return {
        label: "Queued",
        className: "bg-slate-50 text-slate-600 border-slate-200",
        dotClass: "bg-slate-400",
      };
  }
}

export function getTaskStatusBadge(status: TaskStatusType): {
  label: string;
  className: string;
  dotClass: string;
} {
  switch (status) {
    case "completed":
      return {
        label: "Completed",
        className: "bg-emerald-50 text-emerald-700 border-emerald-200",
        dotClass: "bg-emerald-500",
      };
    case "running":
      return {
        label: "Running",
        className: "bg-blue-50 text-blue-700 border-blue-200",
        dotClass: "bg-blue-500 animate-pulse",
      };
    case "ready":
      return {
        label: "Ready",
        className: "bg-indigo-50 text-indigo-700 border-indigo-200",
        dotClass: "bg-indigo-500",
      };
    case "waiting_approval":
      return {
        label: "Needs Approval",
        className: "bg-amber-50 text-amber-800 border-amber-200",
        dotClass: "bg-amber-500 animate-pulse",
      };
    case "retrying":
      return {
        label: "Retrying",
        className: "bg-amber-50 text-amber-700 border-amber-200",
        dotClass: "bg-amber-500",
      };
    case "replanned":
      return {
        label: "Replanned",
        className: "bg-purple-50 text-purple-700 border-purple-200",
        dotClass: "bg-purple-500",
      };
    case "failed":
      return {
        label: "Failed",
        className: "bg-red-50 text-red-700 border-red-200",
        dotClass: "bg-red-500",
      };
    case "cancelled":
      return {
        label: "Cancelled",
        className: "bg-slate-100 text-slate-600 border-slate-200",
        dotClass: "bg-slate-400",
      };
    case "pending":
    default:
      return {
        label: "Pending",
        className: "bg-slate-50 text-slate-600 border-slate-200",
        dotClass: "bg-slate-300",
      };
  }
}

export function getApprovalStatusBadge(status: ApprovalStatusType): {
  label: string;
  className: string;
} {
  switch (status) {
    case "approved":
      return {
        label: "Approved",
        className: "bg-emerald-50 text-emerald-700 border-emerald-200",
      };
    case "rejected":
      return {
        label: "Rejected",
        className: "bg-red-50 text-red-700 border-red-200",
      };
    case "expired":
      return {
        label: "Expired",
        className: "bg-slate-100 text-slate-600 border-slate-200",
      };
    case "pending":
    default:
      return {
        label: "Pending Review",
        className: "bg-amber-50 text-amber-800 border-amber-200 animate-pulse",
      };
  }
}

export function getRiskLevelBadge(risk: RiskLevel): {
  label: string;
  className: string;
} {
  switch (risk) {
    case "critical":
      return {
        label: "Critical Risk",
        className: "bg-red-100 text-red-800 border-red-300 font-semibold",
      };
    case "high":
      return {
        label: "High Risk",
        className: "bg-rose-50 text-rose-700 border-rose-200",
      };
    case "medium":
      return {
        label: "Medium Risk",
        className: "bg-amber-50 text-amber-800 border-amber-200",
      };
    case "low":
    default:
      return {
        label: "Low Risk",
        className: "bg-emerald-50 text-emerald-700 border-emerald-200",
      };
  }
}

export function getMemoryTypeBadge(type: MemoryType): {
  label: string;
  className: string;
} {
  switch (type) {
    case "preference":
      return { label: "Preference", className: "bg-indigo-50 text-indigo-700 border-indigo-200" };
    case "goal":
      return { label: "Goal", className: "bg-blue-50 text-blue-700 border-blue-200" };
    case "task":
      return { label: "Task", className: "bg-sky-50 text-sky-700 border-sky-200" };
    case "result":
      return { label: "Result", className: "bg-emerald-50 text-emerald-700 border-emerald-200" };
    case "private":
      return { label: "Private", className: "bg-rose-50 text-rose-700 border-rose-200" };
    case "shared":
    default:
      return { label: "Shared", className: "bg-slate-50 text-slate-700 border-slate-200" };
  }
}

export function getAgentColor(agentName?: string | null): {
  bg: string;
  text: string;
  border: string;
  pill: string;
} {
  const name = (agentName || "").toLowerCase();
  if (name.includes("email")) {
    return { bg: "bg-blue-50", text: "text-blue-700", border: "border-blue-200", pill: "bg-blue-100 text-blue-800" };
  }
  if (name.includes("coding") || name.includes("code")) {
    return { bg: "bg-violet-50", text: "text-violet-700", border: "border-violet-200", pill: "bg-violet-100 text-violet-800" };
  }
  if (name.includes("browser")) {
    return { bg: "bg-emerald-50", text: "text-emerald-700", border: "border-emerald-200", pill: "bg-emerald-100 text-emerald-800" };
  }
  if (name.includes("calendar")) {
    return { bg: "bg-amber-50", text: "text-amber-700", border: "border-amber-200", pill: "bg-amber-100 text-amber-800" };
  }
  if (name.includes("file")) {
    return { bg: "bg-orange-50", text: "text-orange-700", border: "border-orange-200", pill: "bg-orange-100 text-orange-800" };
  }
  if (name.includes("supervisor")) {
    return { bg: "bg-indigo-50", text: "text-indigo-700", border: "border-indigo-200", pill: "bg-indigo-100 text-indigo-800" };
  }
  if (name.includes("planner")) {
    return { bg: "bg-purple-50", text: "text-purple-700", border: "border-purple-200", pill: "bg-purple-100 text-purple-800" };
  }
  return { bg: "bg-slate-50", text: "text-slate-700", border: "border-slate-200", pill: "bg-slate-100 text-slate-700" };
}

/**
 * Calculates topological execution levels for a list of tasks.
 * Returns an array of columns (levels), where each column contains tasks that can run in parallel.
 */
export function calculateTaskGraphLevels(tasks: ExecutionTask[]): ExecutionTask[][] {
  if (!tasks || tasks.length === 0) return [];

  const taskMap = new Map<number, ExecutionTask>();
  tasks.forEach((t) => taskMap.set(t.id, t));

  const levelMap = new Map<number, number>();

  function getLevel(taskId: number, visited = new Set<number>()): number {
    if (levelMap.has(taskId)) return levelMap.get(taskId)!;
    if (visited.has(taskId)) return 0; // Prevent cycle crash
    visited.add(taskId);

    const task = taskMap.get(taskId);
    if (!task || !task.depends_on || task.depends_on.length === 0) {
      levelMap.set(taskId, 0);
      return 0;
    }

    let maxDepLevel = -1;
    for (const depId of task.depends_on) {
      maxDepLevel = Math.max(maxDepLevel, getLevel(depId, new Set(visited)));
    }

    const calculatedLevel = maxDepLevel + 1;
    levelMap.set(taskId, calculatedLevel);
    return calculatedLevel;
  }

  tasks.forEach((t) => getLevel(t.id));

  const maxLevel = Math.max(...Array.from(levelMap.values()), 0);
  const levels: ExecutionTask[][] = Array.from({ length: maxLevel + 1 }, () => []);

  tasks.forEach((t) => {
    const lvl = levelMap.get(t.id) ?? 0;
    levels[lvl].push(t);
  });

  return levels;
}

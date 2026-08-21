"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { AIOSClient } from "@/lib/api";
import { Goal, ApprovalRequest } from "@/lib/types";
import {
  LayoutDashboard,
  Target,
  CheckSquare,
  Bot,
  ShieldAlert,
  Database,
  CalendarClock,
  Cpu,
  Activity,
  Settings,
  Sparkles,
  ChevronRight
} from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();
  const [pendingApprovalsCount, setPendingApprovalsCount] = useState(0);
  const [activeGoalsCount, setActiveGoalsCount] = useState(0);

  useEffect(() => {
    const updateCounts = () => {
      const approvals = AIOSClient.getApprovals();
      const pending = approvals.filter((a: ApprovalRequest) => a.status === "pending").length;
      setPendingApprovalsCount(pending);

      const goals = AIOSClient.getGoals();
      const active = goals.filter((g: Goal) => g.status === "in_progress").length;
      setActiveGoalsCount(active);
    };

    updateCounts();
    const interval = setInterval(updateCounts, 3000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    {
      label: "Control Center",
      href: "/dashboard",
      icon: LayoutDashboard,
    },
    {
      label: "Autonomous Goals",
      href: "/goals",
      icon: Target,
      badge: activeGoalsCount > 0 ? `${activeGoalsCount}` : undefined,
      badgeColor: "bg-blue-50 text-blue-700 border-blue-200",
    },
    {
      label: "Task Execution",
      href: "/tasks",
      icon: CheckSquare,
    },
    {
      label: "Agent Swarm",
      href: "/agents",
      icon: Bot,
    },
    {
      label: "Human Approvals",
      href: "/approvals",
      icon: ShieldAlert,
      badge: pendingApprovalsCount > 0 ? `${pendingApprovalsCount}` : undefined,
      badgeColor: "bg-amber-500 text-white animate-pulse",
    },
    {
      label: "Shared Memory",
      href: "/memory",
      icon: Database,
    },
    {
      label: "Schedules",
      href: "/schedules",
      icon: CalendarClock,
    },
    {
      label: "Background Jobs",
      href: "/jobs",
      icon: Cpu,
    },
    {
      label: "Telemetry & Audit",
      href: "/activity",
      icon: Activity,
    },
    {
      label: "System Settings",
      href: "/settings",
      icon: Settings,
    },
  ];

  return (
    <aside className="w-64 h-screen bg-white border-r border-slate-200/80 flex flex-col justify-between flex-shrink-0 sticky top-0 select-none z-30">
      {/* Brand Header */}
      <div>
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <Link href="/dashboard" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 rounded-xl bg-slate-950 flex items-center justify-center text-white shadow-sm group-hover:bg-primary-600 transition-colors">
              <Sparkles className="w-4 h-4 text-primary-400 group-hover:text-white" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="text-sm font-bold text-slate-900 tracking-tight">
                  AI OS
                </span>
                <span className="text-[10px] font-semibold uppercase px-1.5 py-0.2 bg-slate-100 text-slate-600 rounded">
                  v2.0
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-medium">Autonomous Swarm</p>
            </div>
          </Link>
        </div>

        {/* Live System Status Pill */}
        <div className="px-4 pt-3.5 pb-2">
          <div className="flex items-center justify-between px-3 py-1.5 rounded-xl bg-slate-50 border border-slate-100 text-[11px]">
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="font-semibold text-slate-700">6 Agents Active</span>
            </div>
            <span className="text-slate-400 font-mono">0.32s Latency</span>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="p-3 space-y-0.5">
          {navItems.map((item) => {
            const isActive =
              pathname === item.href ||
              (item.href !== "/dashboard" && pathname?.startsWith(item.href));
            const Icon = item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-150 group",
                  isActive
                    ? "bg-primary-50 text-primary-700 font-semibold"
                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-50/80"
                )}
              >
                <div className="flex items-center gap-2.5">
                  <Icon
                    className={cn(
                      "w-4 h-4 transition-colors",
                      isActive
                        ? "text-primary-600"
                        : "text-slate-400 group-hover:text-slate-600"
                    )}
                  />
                  <span>{item.label}</span>
                </div>
                <div className="flex items-center gap-1.5">
                  {item.badge && (
                    <span
                      className={cn(
                        "text-[10px] font-bold px-1.5 py-0.5 rounded-full border",
                        item.badgeColor || "bg-slate-100 text-slate-600 border-slate-200"
                      )}
                    >
                      {item.badge}
                    </span>
                  )}
                  {isActive && (
                    <ChevronRight className="w-3.5 h-3.5 text-primary-500" />
                  )}
                </div>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* System Telemetry Footer */}
      <div className="p-4 border-t border-slate-100 bg-slate-50/50">
        <div className="flex items-center justify-between text-[11px] text-slate-500 mb-2">
          <span className="font-medium">Cluster Concurrency</span>
          <span className="font-mono font-semibold text-slate-700">4 / 4 Slots</span>
        </div>
        <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden mb-3">
          <div className="bg-primary-600 h-full rounded-full" style={{ width: "75%" }} />
        </div>
        <div className="flex items-center justify-between pt-2 border-t border-slate-200/60 text-[11px] text-slate-400">
          <span>Supervisor Core</span>
          <span className="text-emerald-600 font-semibold flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" /> Healthy
          </span>
        </div>
      </div>
    </aside>
  );
}

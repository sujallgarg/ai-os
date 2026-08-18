"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Modal } from "@/components/ui/Modal";
import { AIOSClient } from "@/lib/api";
import {
  Search,
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
  Plus
} from "lucide-react";

export interface CommandMenuProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenGoalModal: () => void;
}

export function CommandMenu({ isOpen, onClose, onOpenGoalModal }: CommandMenuProps) {
  const router = useRouter();
  const [query, setQuery] = useState("");

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        if (isOpen) {
          onClose();
        } else {
          // Trigger open via custom event or parent
        }
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  const quickNav = [
    { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { label: "Autonomous Goals", href: "/goals", icon: Target },
    { label: "Task Execution Queue", href: "/tasks", icon: CheckSquare },
    { label: "Agent Swarm Roster", href: "/agents", icon: Bot },
    { label: "Human Approvals Queue", href: "/approvals", icon: ShieldAlert },
    { label: "Shared Agent Memory", href: "/memory", icon: Database },
    { label: "Task Schedules", href: "/schedules", icon: CalendarClock },
    { label: "Background Jobs", href: "/jobs", icon: Cpu },
    { label: "Telemetry & Audit Logs", href: "/activity", icon: Activity },
    { label: "System Settings", href: "/settings", icon: Settings },
  ];

  const goals = AIOSClient.getGoals();
  const filteredGoals = goals.filter((g) =>
    g.title.toLowerCase().includes(query.toLowerCase())
  );

  const filteredNav = quickNav.filter((n) =>
    n.label.toLowerCase().includes(query.toLowerCase())
  );

  const handleSelectNav = (href: string) => {
    onClose();
    router.push(href);
  };

  const handleSelectGoal = (id: string) => {
    onClose();
    router.push(`/goals/${id}`);
  };

  const handleNewGoal = () => {
    onClose();
    onOpenGoalModal();
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="md">
      <div className="space-y-3 -m-1">
        {/* Search Bar */}
        <div className="flex items-center gap-3 px-3 py-2 border-b border-slate-100">
          <Search className="w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type a command, search goals, or jump to a screen..."
            className="w-full text-sm text-slate-900 placeholder:text-slate-400 bg-transparent focus:outline-none"
            autoFocus
          />
          <kbd className="text-[10px] font-mono font-semibold text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">
            ESC
          </kbd>
        </div>

        {/* Action: New Goal */}
        <div className="px-2">
          <button
            onClick={handleNewGoal}
            className="w-full flex items-center gap-2.5 px-3 py-2 text-xs font-semibold text-primary-700 bg-primary-50/50 hover:bg-primary-50 rounded-xl transition-colors text-left"
          >
            <Plus className="w-4 h-4 text-primary-600" />
            <span>Dispatch New Autonomous Goal...</span>
          </button>
        </div>

        {/* Goals Search Results */}
        {filteredGoals.length > 0 && (
          <div className="px-2">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-3 mb-1 block">
              Goals
            </span>
            <div className="space-y-0.5">
              {filteredGoals.slice(0, 3).map((goal) => (
                <button
                  key={goal.id}
                  onClick={() => handleSelectGoal(goal.id)}
                  className="w-full flex items-center justify-between px-3 py-2 text-xs text-slate-700 hover:bg-slate-50 hover:text-slate-900 rounded-xl transition-colors text-left"
                >
                  <div className="flex items-center gap-2 truncate">
                    <Target className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
                    <span className="truncate font-medium">{goal.title}</span>
                  </div>
                  <span className="text-[10px] text-slate-400 font-mono ml-2 flex-shrink-0">
                    {goal.progress}%
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Navigation Links */}
        <div className="px-2 max-h-60 overflow-y-auto">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-3 mb-1 block">
            Navigation
          </span>
          <div className="space-y-0.5">
            {filteredNav.map((nav) => {
              const Icon = nav.icon;
              return (
                <button
                  key={nav.href}
                  onClick={() => handleSelectNav(nav.href)}
                  className="w-full flex items-center gap-2.5 px-3 py-2 text-xs text-slate-700 hover:bg-slate-50 hover:text-slate-900 rounded-xl transition-colors text-left font-medium"
                >
                  <Icon className="w-3.5 h-3.5 text-slate-400" />
                  <span>{nav.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </Modal>
  );
}

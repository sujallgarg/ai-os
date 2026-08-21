"use client";

import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/Button";
import { AIOSClient } from "@/lib/api";
import { AgentProfile, ApprovalRequest } from "@/lib/types";
import {
  Search,
  Plus,
  Bell,
  ShieldAlert,
  Sparkles,
  Bot
} from "lucide-react";
import Link from "next/link";
import { GoalCreationModal } from "@/components/goals/GoalCreationModal";
import { CommandMenu } from "./CommandMenu";

export function Header() {
  const [isGoalModalOpen, setIsGoalModalOpen] = useState(false);
  const [isCommandMenuOpen, setIsCommandMenuOpen] = useState(false);
  const [agents, setAgents] = useState<AgentProfile[]>([]);
  const [pendingApprovals, setPendingApprovals] = useState(0);

  useEffect(() => {
    const refresh = () => {
      setAgents(AIOSClient.getAgents());
      const approvals = AIOSClient.getApprovals();
      setPendingApprovals(approvals.filter((a: ApprovalRequest) => a.status === "pending").length);
    };
    refresh();
    const interval = setInterval(refresh, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <header className="h-16 bg-white/80 backdrop-blur-md border-b border-slate-200/80 sticky top-0 z-20 px-6 flex items-center justify-between">
        {/* Left: Quick Command Search */}
        <div className="flex items-center gap-4 flex-1 max-w-md">
          <button
            onClick={() => setIsCommandMenuOpen(true)}
            className="w-full flex items-center justify-between px-3.5 py-1.5 rounded-xl bg-slate-50 hover:bg-slate-100/80 border border-slate-200/80 text-xs text-slate-500 transition-all shadow-subtle group"
          >
            <div className="flex items-center gap-2">
              <Search className="w-3.5 h-3.5 text-slate-400 group-hover:text-slate-600" />
              <span>Search goals, tasks, agents, memory...</span>
            </div>
            <kbd className="hidden sm:inline-flex text-[10px] font-mono font-semibold text-slate-400 bg-white px-1.5 py-0.5 rounded border border-slate-200 shadow-xs">
              ⌘K
            </kbd>
          </button>
        </div>

        {/* Right: Agent Status & Global Actions */}
        <div className="flex items-center gap-3">
          {/* Agent Swarm Active Avatars */}
          <div className="hidden lg:flex items-center gap-1.5 px-3 py-1 bg-slate-50 border border-slate-100 rounded-xl">
            <span className="text-[11px] font-semibold text-slate-500 mr-1 flex items-center gap-1">
              <Bot className="w-3.5 h-3.5 text-slate-400" /> Swarm:
            </span>
            <div className="flex -space-x-1.5">
              {agents.slice(0, 5).map((agent) => {
                const isBusy = agent.status === "busy";
                return (
                  <Link
                    key={agent.id}
                    href={`/agents/${agent.id}`}
                    title={`${agent.name} (${agent.status}): ${agent.current_task || "Idle"}`}
                    className="relative group"
                  >
                    <div
                      className={`w-6 h-6 rounded-full border-2 border-white flex items-center justify-center text-[10px] font-bold text-white uppercase ${
                        agent.avatar_bg || "bg-slate-700"
                      }`}
                    >
                      {agent.name.charAt(0)}
                    </div>
                    {isBusy && (
                      <span className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-blue-500 ring-2 ring-white animate-pulse" />
                    )}
                  </Link>
                );
              })}
            </div>
          </div>

          {/* Pending Approvals Quick Alert */}
          {pendingApprovals > 0 && (
            <Link
              href="/approvals"
              className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-amber-50 hover:bg-amber-100/80 border border-amber-200 text-amber-800 text-xs font-semibold transition-colors"
            >
              <ShieldAlert className="w-3.5 h-3.5 text-amber-600 animate-pulse" />
              <span>{pendingApprovals} Approvals</span>
            </Link>
          )}

          {/* New Goal Primary Button */}
          <Button
            variant="primary"
            size="sm"
            onClick={() => setIsGoalModalOpen(true)}
            leftIcon={<Plus className="w-3.5 h-3.5" />}
            className="shadow-sm"
          >
            New Goal
          </Button>
        </div>
      </header>

      {/* Goal Creation Modal */}
      <GoalCreationModal
        isOpen={isGoalModalOpen}
        onClose={() => setIsGoalModalOpen(false)}
      />

      {/* Command Menu Modal */}
      <CommandMenu
        isOpen={isCommandMenuOpen}
        onClose={() => setIsCommandMenuOpen(false)}
        onOpenGoalModal={() => setIsGoalModalOpen(true)}
      />
    </>
  );
}

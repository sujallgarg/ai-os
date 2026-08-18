"use client";

import React from "react";
import Link from "next/link";
import { AgentProfile } from "@/lib/types";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { Bot, ArrowRight, CheckCircle2, Clock } from "lucide-react";
import { cn } from "@/lib/utils";

export interface AgentSwarmCardProps {
  agents: AgentProfile[];
}

export function AgentSwarmCard({ agents }: AgentSwarmCardProps) {
  return (
    <Card className="flex flex-col justify-between">
      <div>
        <CardHeader>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center">
              <Bot className="w-4 h-4" />
            </div>
            <div>
              <CardTitle>Autonomous Agent Swarm</CardTitle>
              <CardDescription>Real-time telemetry and capability load</CardDescription>
            </div>
          </div>
          <Link
            href="/agents"
            className="text-xs font-semibold text-primary-600 hover:text-primary-800 flex items-center gap-1 group"
          >
            <span>View all</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
          </Link>
        </CardHeader>

        <div className="space-y-3">
          {agents.map((agent) => {
            const isBusy = agent.status === "busy";
            return (
              <Link
                key={agent.id}
                href={`/agents/${agent.id}`}
                className="flex items-center justify-between p-3 rounded-xl border border-slate-100 hover:border-slate-200 hover:bg-slate-50/70 transition-all duration-150 group"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div
                    className={cn(
                      "w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold text-white uppercase flex-shrink-0",
                      agent.avatar_bg || "bg-slate-700"
                    )}
                  >
                    {agent.name.charAt(0)}
                  </div>
                  <div className="min-w-0">
                    <div className="flex items-center gap-1.5">
                      <span className="text-xs font-semibold text-slate-800 group-hover:text-primary-700 truncate">
                        {agent.name}
                      </span>
                      <span
                        className={cn(
                          "w-1.5 h-1.5 rounded-full flex-shrink-0",
                          isBusy ? "bg-blue-500 animate-pulse" : "bg-emerald-500"
                        )}
                      />
                    </div>
                    <p className="text-[11px] text-slate-400 truncate">
                      {agent.current_task || agent.role}
                    </p>
                  </div>
                </div>

                <div className="text-right flex-shrink-0 ml-3">
                  <span className="text-[11px] font-mono font-semibold text-slate-700 block">
                    {agent.total_executed} tasks
                  </span>
                  <span className="text-[10px] text-slate-400 font-mono">
                    {agent.success_rate}% success
                  </span>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
        <span>Capability registry: <strong>32 tools active</strong></span>
        <span className="text-emerald-600 font-semibold flex items-center gap-1">
          <CheckCircle2 className="w-3.5 h-3.5" /> All systems nominal
        </span>
      </div>
    </Card>
  );
}

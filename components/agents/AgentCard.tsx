"use client";

import React from "react";
import Link from "next/link";
import { AgentProfile } from "@/lib/types";
import { Card } from "@/components/ui/Card";
import { Bot, ArrowRight, Wrench, Shield, Zap } from "lucide-react";
import { cn } from "@/lib/utils";

export interface AgentCardProps {
  agent: AgentProfile;
}

export function AgentCard({ agent }: AgentCardProps) {
  const isBusy = agent.status === "busy";

  return (
    <Link
      href={`/agents/${agent.id}`}
      className="block group bg-white border border-slate-200/80 hover:border-primary-300/80 rounded-2xl p-5 shadow-card hover:shadow-elevated transition-all duration-200"
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-3">
          <div
            className={cn(
              "w-10 h-10 rounded-2xl flex items-center justify-center text-sm font-bold text-white uppercase shadow-sm flex-shrink-0",
              agent.avatar_bg || "bg-slate-700"
            )}
          >
            {agent.name.charAt(0)}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-sm font-bold text-slate-900 group-hover:text-primary-700 transition-colors">
                {agent.name}
              </h3>
              <span
                className={cn(
                  "text-[10px] font-semibold px-2 py-0.2 rounded-full border",
                  isBusy
                    ? "bg-blue-50 text-blue-700 border-blue-200"
                    : "bg-emerald-50 text-emerald-700 border-emerald-200"
                )}
              >
                {agent.status}
              </span>
            </div>
            <span className="text-xs text-slate-500 font-medium">{agent.role}</span>
          </div>
        </div>
        <div className="w-8 h-8 rounded-xl bg-slate-50 group-hover:bg-primary-50 text-slate-400 group-hover:text-primary-600 flex items-center justify-center transition-colors flex-shrink-0">
          <ArrowRight className="w-4 h-4" />
        </div>
      </div>

      <p className="text-xs text-slate-500 line-clamp-2 mb-4 leading-relaxed">
        {agent.description}
      </p>

      {/* Metrics Row */}
      <div className="grid grid-cols-3 gap-2 p-2.5 bg-slate-50 rounded-xl border border-slate-100 mb-4 text-center">
        <div>
          <span className="text-[10px] text-slate-400 uppercase font-semibold block">Executed</span>
          <span className="text-xs font-bold text-slate-800 font-mono">{agent.total_executed}</span>
        </div>
        <div>
          <span className="text-[10px] text-slate-400 uppercase font-semibold block">Success</span>
          <span className="text-xs font-bold text-emerald-700 font-mono">{agent.success_rate}%</span>
        </div>
        <div>
          <span className="text-[10px] text-slate-400 uppercase font-semibold block">Latency</span>
          <span className="text-xs font-bold text-slate-800 font-mono">{agent.avg_latency_ms}ms</span>
        </div>
      </div>

      {/* Capabilities Snippet */}
      <div>
        <div className="flex items-center justify-between text-[11px] text-slate-500 mb-1.5 font-medium">
          <span className="flex items-center gap-1">
            <Zap className="w-3 h-3 text-primary-600" /> Capabilities ({agent.capabilities.length})
          </span>
          <span className="flex items-center gap-1 font-mono text-slate-400">
            <Wrench className="w-3 h-3" /> {agent.tools.length} Tools
          </span>
        </div>
        <div className="flex flex-wrap gap-1">
          {agent.capabilities.slice(0, 3).map((cap) => (
            <span
              key={cap}
              className="text-[10px] font-mono bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded border border-slate-200"
            >
              {cap}
            </span>
          ))}
          {agent.capabilities.length > 3 && (
            <span className="text-[10px] font-mono bg-slate-50 text-slate-400 px-1 py-0.5 rounded">
              +{agent.capabilities.length - 3} more
            </span>
          )}
        </div>
      </div>
    </Link>
  );
}

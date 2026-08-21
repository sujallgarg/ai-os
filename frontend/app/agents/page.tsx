"use client";

import React, { useEffect, useState } from "react";
import { AIOSClient } from "@/lib/api";
import { AgentProfile } from "@/lib/types";
import { AgentCard } from "@/components/agents/AgentCard";
import { Bot, Wrench, Zap, CheckCircle2 } from "lucide-react";

export default function AgentsPage() {
  const [agents, setAgents] = useState<AgentProfile[]>([]);

  useEffect(() => {
    setAgents(AIOSClient.getAgents());
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Agent Swarm Roster
            </h1>
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-violet-50 text-violet-700 border border-violet-200">
              {agents.length} Specialized Agents
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 max-w-xl">
            Autonomous agent units equipped with distinct capability signatures, sandbox tools, and shared memory permissions.
          </p>
        </div>
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {agents.map((agent) => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </div>
    </div>
  );
}

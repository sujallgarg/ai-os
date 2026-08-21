"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { AIOSClient } from "@/lib/api";
import { AgentProfile, ExecutionTask } from "@/lib/types";
import { TaskTable } from "@/components/tasks/TaskTable";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { ArrowLeft, Bot, Wrench, Zap, Shield, Database, Cpu, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";

export default function AgentDetailPage() {
  const params = useParams();
  const agentId = params.id as string;

  const [agent, setAgent] = useState<AgentProfile | null>(null);
  const [tasks, setTasks] = useState<ExecutionTask[]>([]);

  useEffect(() => {
    const found = AIOSClient.getAgent(agentId);
    if (found) setAgent(found);

    const goals = AIOSClient.getGoals();
    const agentTasks = goals.flatMap((g) => g.tasks).filter((t) => t.agent === agentId);
    setTasks(agentTasks);
  }, [agentId]);

  if (!agent) {
    return (
      <div className="py-16 text-center space-y-3">
        <p className="text-sm text-slate-500">Agent not found.</p>
        <Link href="/agents" className="text-xs text-primary-600 font-semibold hover:underline">
          Return to Agent Swarm
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Nav */}
      <Link
        href="/agents"
        className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-900 transition-colors"
      >
        <ArrowLeft className="w-3.5 h-3.5" />
        <span>Back to Agent Swarm</span>
      </Link>

      {/* Hero Agent Profile Card */}
      <div className="bg-white border border-slate-200/90 rounded-3xl p-6 sm:p-8 shadow-card space-y-6">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div className="flex items-center gap-4">
            <div
              className={cn(
                "w-16 h-16 rounded-3xl flex items-center justify-center text-2xl font-bold text-white uppercase shadow-md",
                agent.avatar_bg || "bg-slate-700"
              )}
            >
              {agent.name.charAt(0)}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
                  {agent.name}
                </h1>
                <span
                  className={cn(
                    "text-xs px-2.5 py-0.5 rounded-full font-semibold border",
                    agent.status === "busy"
                      ? "bg-blue-50 text-blue-700 border-blue-200"
                      : "bg-emerald-50 text-emerald-700 border-emerald-200"
                  )}
                >
                  {agent.status}
                </span>
              </div>
              <p className="text-xs sm:text-sm text-slate-500 font-medium">{agent.role}</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400 font-mono bg-slate-50 border border-slate-100 px-3 py-1.5 rounded-xl">
              Priority Tier: <strong className="text-slate-800">{agent.priority} / 10</strong>
            </span>
          </div>
        </div>

        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed max-w-3xl">
          {agent.description}
        </p>

        {/* Telemetry Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 bg-slate-50 rounded-2xl border border-slate-100 text-center">
          <div>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">Tasks Executed</span>
            <span className="text-lg font-bold text-slate-900 font-mono">{agent.total_executed}</span>
          </div>
          <div>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">Success Rate</span>
            <span className="text-lg font-bold text-emerald-700 font-mono">{agent.success_rate}%</span>
          </div>
          <div>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">Avg Latency</span>
            <span className="text-lg font-bold text-slate-900 font-mono">{agent.avg_latency_ms}ms</span>
          </div>
          <div>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">Memory Types</span>
            <span className="text-lg font-bold text-slate-900 font-mono">{agent.memory_types.length}</span>
          </div>
        </div>
      </div>

      {/* Two-Column Grid: Capabilities + Sandbox Tools */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Capabilities */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-primary-600" />
              <CardTitle>Registered Capability Signatures ({agent.capabilities.length})</CardTitle>
            </div>
          </CardHeader>
          <div className="flex flex-wrap gap-2">
            {agent.capabilities.map((cap) => (
              <span
                key={cap}
                className="text-xs font-mono bg-slate-50 text-slate-800 border border-slate-200 px-3 py-1.5 rounded-xl font-medium"
              >
                {cap}
              </span>
            ))}
          </div>
        </Card>

        {/* Tools */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Wrench className="w-4 h-4 text-violet-600" />
              <CardTitle>Accessible Toolsets & Sandbox ({agent.tools.length})</CardTitle>
            </div>
          </CardHeader>
          <div className="flex flex-wrap gap-2">
            {agent.tools.map((tool) => (
              <span
                key={tool}
                className="text-xs font-mono bg-violet-50 text-violet-800 border border-violet-200 px-3 py-1.5 rounded-xl font-medium"
              >
                {tool}
              </span>
            ))}
          </div>
        </Card>
      </div>

      {/* Agent Task History */}
      <div>
        <div className="flex items-center gap-2 mb-3">
          <Cpu className="w-4 h-4 text-slate-600" />
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
            Tasks Handled by {agent.name} ({tasks.length})
          </h2>
        </div>
        <TaskTable tasks={tasks} />
      </div>
    </div>
  );
}

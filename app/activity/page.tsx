"use client";

import React, { useEffect, useState } from "react";
import { AIOSClient } from "@/lib/api";
import { ActivityEvent } from "@/lib/types";
import { formatRelativeTime, formatDate, cn } from "@/lib/utils";
import { Activity, CheckCircle2, AlertTriangle, ShieldCheck, Play, Database, RefreshCw, Filter, Search } from "lucide-react";
import { Tabs } from "@/components/ui/Tabs";

export default function ActivityPage() {
  const [activities, setActivities] = useState<ActivityEvent[]>([]);
  const [activeTab, setActiveTab] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");

  const fetchActivities = () => {
    setActivities(AIOSClient.getActivity());
  };

  useEffect(() => {
    fetchActivities();
    const interval = setInterval(fetchActivities, 3000);
    return () => clearInterval(interval);
  }, []);

  const getEventIcon = (type: ActivityEvent["event_type"], severity: ActivityEvent["severity"]) => {
    switch (type) {
      case "task_completed":
        return <CheckCircle2 className="w-4 h-4 text-emerald-600" />;
      case "approval_required":
        return <AlertTriangle className="w-4 h-4 text-amber-600" />;
      case "approval_granted":
        return <ShieldCheck className="w-4 h-4 text-emerald-600" />;
      case "task_started":
        return <Play className="w-4 h-4 text-blue-600" />;
      case "memory_write":
        return <Database className="w-4 h-4 text-indigo-600" />;
      case "replan":
        return <RefreshCw className="w-4 h-4 text-purple-600" />;
      default:
        return <Activity className="w-4 h-4 text-slate-500" />;
    }
  };

  const filteredActivities = activities.filter((act) => {
    const matchesSearch =
      act.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      act.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (act.agent_name && act.agent_name.toLowerCase().includes(searchQuery.toLowerCase()));

    if (activeTab === "approvals") return matchesSearch && act.event_type.startsWith("approval");
    if (activeTab === "tasks") return matchesSearch && act.event_type.startsWith("task");
    if (activeTab === "memory") return matchesSearch && act.event_type === "memory_write";
    return matchesSearch;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Telemetry & Audit Log Stream
          </h1>
          <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
            {activities.length} Recorded Events
          </span>
        </div>
        <p className="text-xs sm:text-sm text-slate-500 max-w-xl">
          Complete, chronological stream of all autonomous system events, state transitions, tool invocations, and operator approvals.
        </p>
      </div>

      {/* Tabs & Search */}
      <div className="flex items-center justify-between gap-4 flex-wrap pb-2 border-b border-slate-200/80">
        <Tabs
          tabs={[
            { id: "all", label: "All Telemetry", count: activities.length },
            { id: "tasks", label: "Task Events" },
            { id: "approvals", label: "Approval Events" },
            { id: "memory", label: "Memory Writes" },
          ]}
          activeTab={activeTab}
          onChange={setActiveTab}
          className="border-b-0"
        />

        <div className="relative min-w-[240px]">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Filter audit events..."
            className="w-full bg-white border border-slate-200 rounded-xl pl-9 pr-3.5 py-1.5 text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-500/10"
          />
        </div>
      </div>

      {/* Activity Timeline List */}
      <div className="bg-white border border-slate-200/90 rounded-2xl shadow-card p-4 divide-y divide-slate-100">
        {filteredActivities.length === 0 ? (
          <div className="p-8 text-center text-slate-400 text-xs">
            No events found matching your filter criteria.
          </div>
        ) : (
          filteredActivities.map((act) => (
            <div
              key={act.id}
              className="flex items-start gap-3.5 py-3.5 px-2 hover:bg-slate-50/80 rounded-xl transition-colors"
            >
              <div className="w-8 h-8 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                {getEventIcon(act.event_type, act.severity)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-xs font-bold text-slate-900 truncate">
                    {act.title}
                  </span>
                  <span className="text-[11px] text-slate-400 font-mono flex-shrink-0">
                    {formatDate(act.timestamp)} ({formatRelativeTime(act.timestamp)})
                  </span>
                </div>
                <p className="text-xs text-slate-600 mt-0.5 leading-relaxed">
                  {act.description}
                </p>
                <div className="flex items-center gap-3 mt-1.5 text-[10px] text-slate-400 font-mono">
                  {act.agent_name && (
                    <span>Agent: <strong className="text-slate-700">{act.agent_name}</strong></span>
                  )}
                  {act.goal_id && (
                    <span>Goal: <strong className="text-slate-700">{act.goal_id}</strong></span>
                  )}
                  {act.task_id && (
                    <span>Task: <strong className="text-slate-700">#{act.task_id}</strong></span>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

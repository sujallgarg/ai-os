"use client";

import { useState } from "react";
import { useRealtime, RealtimeEvent } from "@/hooks/useRealtime";
import { Bot, ChevronDown, ChevronUp, CheckCircle2, Clock, ShieldAlert, Sparkles } from "lucide-react";

export default function LiveActivity({ jobId }: { jobId?: string }) {
  const { events, isConnected } = useRealtime(jobId);
  const [collapsed, setCollapsed] = useState(false);

  // Find active task or recent event
  const latestEvent: RealtimeEvent | undefined = events[0];
  const activeAgent = latestEvent?.data?.agent_id || latestEvent?.data?.metadata?.agent || "AI Team";
  const activeTask = latestEvent?.data?.metadata?.description || latestEvent?.data?.description || latestEvent?.event || "Idle";
  const progress = latestEvent?.data?.progress ?? latestEvent?.progress ?? 0;

  if (events.length === 0 && !isConnected) {
    return null;
  }

  return (
    <div className="fixed bottom-6 right-6 z-50 w-80 sm:w-96 rounded-2xl border border-indigo-100 bg-white/95 p-4 shadow-2xl backdrop-blur transition-all duration-300">
      {/* Header Bar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="relative flex h-2.5 w-2.5">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
            <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500" />
          </span>

          <span className="text-xs font-semibold uppercase tracking-wider text-slate-900 flex items-center gap-1.5">
            <Sparkles size={13} className="text-indigo-600" />
            Live AI Activity
          </span>
        </div>

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
        >
          {collapsed ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>
      </div>

      {/* Main Body */}
      {!collapsed && (
        <div className="mt-3 space-y-3">
          {/* Active Agent Info */}
          <div className="flex items-center gap-3 rounded-xl bg-indigo-50/70 p-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-white shadow-sm">
              <Bot size={16} />
            </div>

            <div className="flex-1 overflow-hidden">
              <p className="text-xs font-bold text-slate-950 truncate capitalize">
                {activeAgent}
              </p>
              <p className="text-xs text-indigo-700 truncate">
                {activeTask}
              </p>
            </div>
          </div>

          {/* Progress Bar */}
          {progress > 0 && (
            <div className="space-y-1">
              <div className="flex justify-between text-[11px] font-medium text-slate-500">
                <span>Progress</span>
                <span>{Math.round(progress)}%</span>
              </div>
              <div className="h-1.5 overflow-hidden rounded-full bg-slate-100">
                <div
                  className="h-full rounded-full bg-indigo-600 transition-all duration-500"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          )}

          {/* Event Stream Log */}
          <div className="max-h-36 space-y-1.5 overflow-y-auto pr-1 text-xs">
            {events.slice(0, 4).map((evt, idx) => (
              <div key={idx} className="flex items-start gap-2 text-slate-600">
                {evt.event.includes("completed") ? (
                  <CheckCircle2 size={13} className="mt-0.5 text-emerald-500 flex-shrink-0" />
                ) : evt.event.includes("approval") ? (
                  <ShieldAlert size={13} className="mt-0.5 text-amber-500 flex-shrink-0" />
                ) : (
                  <Clock size={13} className="mt-0.5 text-indigo-500 flex-shrink-0" />
                )}

                <span className="truncate">
                  {evt.data?.metadata?.description || evt.data?.message || evt.event}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

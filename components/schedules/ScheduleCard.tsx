"use client";

import React from "react";
import { ScheduledTask } from "@/lib/types";
import { formatRelativeTime, cn } from "@/lib/utils";
import { Button } from "@/components/ui/Button";
import { Switch } from "@/components/ui/Switch";
import { CalendarClock, Play, Clock, Repeat, Bot } from "lucide-react";
import { AIOSClient } from "@/lib/api";

export interface ScheduleCardProps {
  schedule: ScheduledTask;
  onToggled?: () => void;
  onRunNow?: () => void;
}

export function ScheduleCard({ schedule, onToggled, onRunNow }: ScheduleCardProps) {
  const handleToggle = () => {
    AIOSClient.toggleSchedule(schedule.id);
    if (onToggled) onToggled();
  };

  const handleRun = () => {
    AIOSClient.runScheduleNow(schedule.id);
    if (onRunNow) onRunNow();
  };

  return (
    <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-card hover:shadow-elevated transition-all flex flex-col justify-between">
      <div>
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-slate-50 border border-slate-100 text-slate-700 flex items-center justify-center flex-shrink-0">
              <CalendarClock className="w-5 h-5 text-primary-600" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-slate-900">
                  {schedule.name}
                </h3>
                <span
                  className={cn(
                    "text-[10px] font-semibold px-2 py-0.2 rounded-full border",
                    schedule.enabled
                      ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                      : "bg-slate-100 text-slate-500 border-slate-200"
                  )}
                >
                  {schedule.enabled ? "Active" : "Paused"}
                </span>
              </div>
              <span className="text-xs font-mono text-slate-400">
                {schedule.cron_or_interval}
              </span>
            </div>
          </div>
          <Switch checked={schedule.enabled} onChange={handleToggle} />
        </div>

        <p className="text-xs text-slate-600 bg-slate-50 p-3 rounded-xl border border-slate-100 mb-4 leading-relaxed">
          {schedule.goal_prompt}
        </p>

        <div className="space-y-1 text-xs text-slate-500 mb-4">
          <div className="flex justify-between">
            <span className="text-slate-400">Target Agent:</span>
            <span className="font-semibold text-slate-700 capitalize">{schedule.target_agent || "Supervisor"}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Next Scheduled Run:</span>
            <span className="font-mono text-slate-700">{formatRelativeTime(schedule.next_run)}</span>
          </div>
          {schedule.last_run && (
            <div className="flex justify-between">
              <span className="text-slate-400">Last Triggered:</span>
              <span className="font-mono text-slate-700">{formatRelativeTime(schedule.last_run)}</span>
            </div>
          )}
        </div>
      </div>

      <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
        <span className="text-[11px] text-slate-400 font-medium flex items-center gap-1">
          <Repeat className="w-3.5 h-3.5" /> Recurring Cron
        </span>
        <Button
          size="sm"
          variant="outline"
          onClick={handleRun}
          leftIcon={<Play className="w-3 h-3 text-primary-600" />}
        >
          Run Now
        </Button>
      </div>
    </div>
  );
}

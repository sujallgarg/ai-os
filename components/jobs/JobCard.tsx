"use client";

import React, { useState } from "react";
import { Job } from "@/lib/types";
import { formatRelativeTime, cn } from "@/lib/utils";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { Cpu, Terminal, CheckCircle2, RotateCw, AlertCircle, XCircle } from "lucide-react";

export interface JobCardProps {
  job: Job;
}

export function JobCard({ job }: JobCardProps) {
  const [isLogsOpen, setIsLogsOpen] = useState(false);

  const getStatusBadge = () => {
    switch (job.status) {
      case "completed":
        return {
          label: "Completed",
          className: "bg-emerald-50 text-emerald-700 border-emerald-200",
          icon: <CheckCircle2 className="w-3.5 h-3.5" />,
        };
      case "running":
        return {
          label: "Executing",
          className: "bg-blue-50 text-blue-700 border-blue-200",
          icon: <RotateCw className="w-3.5 h-3.5 animate-spin" />,
        };
      case "failed":
        return {
          label: "Failed",
          className: "bg-red-50 text-red-700 border-red-200",
          icon: <AlertCircle className="w-3.5 h-3.5" />,
        };
      case "cancelled":
      default:
        return {
          label: "Cancelled",
          className: "bg-slate-100 text-slate-600 border-slate-200",
          icon: <XCircle className="w-3.5 h-3.5" />,
        };
    }
  };

  const badge = getStatusBadge();

  return (
    <>
      <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-card hover:shadow-elevated transition-all flex flex-col justify-between">
        <div>
          <div className="flex items-start justify-between gap-3 mb-3">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[11px] font-mono font-bold text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded">
                  {job.id}
                </span>
                <span className={cn("text-[11px] px-2 py-0.5 rounded-full font-semibold border flex items-center gap-1", badge.className)}>
                  {badge.icon}
                  {badge.label}
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900 line-clamp-1">
                {job.goal}
              </h3>
            </div>
            <span className="text-xs text-slate-400 font-mono">
              {formatRelativeTime(job.created_at)}
            </span>
          </div>

          <div className="space-y-1.5 my-4">
            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-500 font-medium">Job Execution Progress</span>
              <span className="font-mono font-bold text-slate-800">{job.progress}%</span>
            </div>
            <ProgressBar value={job.progress} color={job.status === "completed" ? "emerald" : "primary"} size="sm" />
          </div>

          {/* Latest Log Snippet */}
          {job.logs.length > 0 && (
            <div className="bg-slate-900 text-slate-200 p-3 rounded-xl text-[11px] font-mono mb-4 flex items-start gap-2 overflow-hidden">
              <Terminal className="w-3.5 h-3.5 text-primary-400 flex-shrink-0 mt-0.5" />
              <span className="truncate text-slate-300">
                {job.logs[job.logs.length - 1].message}
              </span>
            </div>
          )}
        </div>

        <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
          <span className="text-[11px] text-slate-400 font-mono">
            {job.logs.length} telemetry entries
          </span>
          <Button
            size="sm"
            variant="outline"
            onClick={() => setIsLogsOpen(true)}
            leftIcon={<Terminal className="w-3 h-3" />}
          >
            Live Logs
          </Button>
        </div>
      </div>

      {/* Logs Modal */}
      <Modal
        isOpen={isLogsOpen}
        onClose={() => setIsLogsOpen(false)}
        size="lg"
        title={
          <div className="flex items-center gap-2">
            <Terminal className="w-5 h-5 text-primary-600" />
            <span>Job Execution Log Stream</span>
          </div>
        }
        description={`Job ID: ${job.id} • ${job.goal}`}
        footer={
          <Button variant="outline" size="md" onClick={() => setIsLogsOpen(false)}>
            Close
          </Button>
        }
      >
        <div className="bg-slate-950 text-slate-100 p-4 rounded-2xl font-mono text-xs space-y-2 max-h-96 overflow-y-auto">
          {job.logs.map((log, idx) => (
            <div key={idx} className="flex items-start gap-3 leading-relaxed">
              <span className="text-slate-500 flex-shrink-0 select-none">[{log.timestamp}]</span>
              <span
                className={
                  log.level === "error"
                    ? "text-red-400"
                    : log.level === "warn"
                    ? "text-amber-300"
                    : "text-slate-200"
                }
              >
                {log.message}
              </span>
            </div>
          ))}
        </div>
      </Modal>
    </>
  );
}

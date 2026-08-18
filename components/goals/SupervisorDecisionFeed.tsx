"use client";

import React from "react";
import { ShieldCheck, ArrowRight, AlertTriangle, CheckCircle, RefreshCw } from "lucide-react";
import { formatRelativeTime } from "@/lib/utils";

export interface SupervisorDecisionFeedProps {
  decision?: {
    action: string;
    reason: string;
    timestamp: string;
  };
}

export function SupervisorDecisionFeed({ decision }: SupervisorDecisionFeedProps) {
  if (!decision) return null;

  const getActionPill = (action: string) => {
    switch (action) {
      case "COMPLETE":
        return {
          label: "COMPLETE",
          bg: "bg-emerald-50 text-emerald-800 border-emerald-200",
          icon: <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />,
        };
      case "REPLAN":
        return {
          label: "REPLAN",
          bg: "bg-purple-50 text-purple-800 border-purple-200",
          icon: <RefreshCw className="w-3.5 h-3.5 text-purple-600" />,
        };
      case "ASK_USER":
        return {
          label: "APPROVAL REQUIRED",
          bg: "bg-amber-50 text-amber-800 border-amber-200",
          icon: <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />,
        };
      case "CONTINUE":
      default:
        return {
          label: "CONTINUE",
          bg: "bg-blue-50 text-blue-800 border-blue-200",
          icon: <ShieldCheck className="w-3.5 h-3.5 text-blue-600" />,
        };
    }
  };

  const pill = getActionPill(decision.action);

  return (
    <div className="bg-white border border-slate-200/80 rounded-2xl p-4 shadow-subtle flex items-start justify-between gap-4">
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600 mt-0.5">
          <ShieldCheck className="w-4 h-4 text-primary-600" />
        </div>
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-bold text-slate-900">
              Supervisor Telemetry Decision
            </span>
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md border flex items-center gap-1 ${pill.bg}`}>
              {pill.icon}
              {pill.label}
            </span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            {decision.reason}
          </p>
        </div>
      </div>
      <span className="text-[11px] text-slate-400 font-mono whitespace-nowrap">
        {formatRelativeTime(decision.timestamp)}
      </span>
    </div>
  );
}

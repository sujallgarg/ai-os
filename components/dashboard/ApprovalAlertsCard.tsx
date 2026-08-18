"use client";

import React from "react";
import Link from "next/link";
import { ApprovalRequest } from "@/lib/types";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { getRiskLevelBadge, formatRelativeTime, cn } from "@/lib/utils";
import { ShieldAlert, ArrowRight, Check, X, ShieldCheck } from "lucide-react";
import { AIOSClient } from "@/lib/api";

export interface ApprovalAlertsCardProps {
  approvals: ApprovalRequest[];
  onApprovalHandled?: () => void;
}

export function ApprovalAlertsCard({ approvals, onApprovalHandled }: ApprovalAlertsCardProps) {
  const pending = approvals.filter((a) => a.status === "pending");

  const handleApprove = (id: string, e: React.MouseEvent) => {
    e.preventDefault();
    AIOSClient.approveRequest(id);
    if (onApprovalHandled) onApprovalHandled();
  };

  const handleReject = (id: string, e: React.MouseEvent) => {
    e.preventDefault();
    AIOSClient.rejectRequest(id);
    if (onApprovalHandled) onApprovalHandled();
  };

  return (
    <Card className="flex flex-col justify-between">
      <div>
        <CardHeader>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
              <ShieldAlert className="w-4 h-4" />
            </div>
            <div>
              <CardTitle>Human-in-the-Loop Approvals</CardTitle>
              <CardDescription>Security policy permission gates</CardDescription>
            </div>
          </div>
          <Link
            href="/approvals"
            className="text-xs font-semibold text-primary-600 hover:text-primary-800 flex items-center gap-1 group"
          >
            <span>View all ({pending.length})</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
          </Link>
        </CardHeader>

        {pending.length === 0 ? (
          <div className="py-8 text-center bg-slate-50 border border-slate-100 rounded-2xl">
            <ShieldCheck className="w-8 h-8 text-emerald-500 mx-auto mb-2" />
            <span className="text-xs font-semibold text-slate-700 block">
              No Pending Approval Requests
            </span>
            <span className="text-[11px] text-slate-400">
              Autonomous execution running within policy limits
            </span>
          </div>
        ) : (
          <div className="space-y-3">
            {pending.slice(0, 3).map((req) => {
              const risk = getRiskLevelBadge(req.risk_level);
              return (
                <div
                  key={req.id}
                  className="p-3.5 rounded-xl border border-amber-200/80 bg-amber-50/30 hover:bg-amber-50/50 transition-all space-y-2.5"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-1.5 mb-1">
                        <span className="text-xs font-bold text-slate-900">
                          {req.action}
                        </span>
                        <span className={cn("text-[10px] px-2 py-0.2 rounded-md font-semibold border", risk.className)}>
                          {risk.label}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-600 leading-snug">
                        {req.reason}
                      </p>
                    </div>
                    <span className="text-[10px] text-slate-400 font-mono flex-shrink-0">
                      {formatRelativeTime(req.created_at)}
                    </span>
                  </div>

                  <div className="flex items-center justify-between pt-2 border-t border-amber-200/60">
                    <span className="text-[10px] font-mono text-slate-500">
                      Tool: <strong className="text-slate-800">{req.tool_name}</strong>
                    </span>
                    <div className="flex items-center gap-1.5">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={(e) => handleReject(req.id, e)}
                        className="h-7 text-xs text-red-700 border-red-200 hover:bg-red-50"
                      >
                        <X className="w-3 h-3 mr-1" /> Deny
                      </Button>
                      <Button
                        size="sm"
                        variant="primary"
                        onClick={(e) => handleApprove(req.id, e)}
                        className="h-7 text-xs bg-emerald-600 hover:bg-emerald-700 text-white"
                      >
                        <Check className="w-3 h-3 mr-1" /> Approve
                      </Button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
        <span>Policy: <strong>Default ASK_USER for send/write</strong></span>
        <Link href="/settings" className="text-slate-400 hover:text-slate-700">
          Configure rules
        </Link>
      </div>
    </Card>
  );
}

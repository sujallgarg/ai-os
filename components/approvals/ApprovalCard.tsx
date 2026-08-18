"use client";

import React, { useState } from "react";
import { ApprovalRequest } from "@/lib/types";
import { getRiskLevelBadge, formatRelativeTime, cn } from "@/lib/utils";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { ShieldAlert, Check, X, Eye, Lock } from "lucide-react";
import { AIOSClient } from "@/lib/api";

export interface ApprovalCardProps {
  approval: ApprovalRequest;
  onHandled?: () => void;
}

export function ApprovalCard({ approval, onHandled }: ApprovalCardProps) {
  const [isDetailOpen, setIsDetailOpen] = useState(false);
  const isPending = approval.status === "pending";
  const risk = getRiskLevelBadge(approval.risk_level);

  const handleApprove = () => {
    AIOSClient.approveRequest(approval.id);
    setIsDetailOpen(false);
    if (onHandled) onHandled();
  };

  const handleReject = () => {
    AIOSClient.rejectRequest(approval.id);
    setIsDetailOpen(false);
    if (onHandled) onHandled();
  };

  return (
    <>
      <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-card hover:shadow-elevated transition-all flex flex-col justify-between">
        <div>
          {/* Header */}
          <div className="flex items-start justify-between gap-3 mb-3">
            <div>
              <div className="flex items-center gap-2 mb-1 flex-wrap">
                <span className="text-[11px] font-mono font-bold text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded">
                  {approval.id}
                </span>
                <span className={cn("text-xs px-2.5 py-0.5 rounded-full font-semibold border", risk.className)}>
                  {risk.label}
                </span>
                <span
                  className={cn(
                    "text-xs px-2.5 py-0.5 rounded-full font-semibold border capitalize",
                    approval.status === "approved"
                      ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                      : approval.status === "rejected"
                      ? "bg-red-50 text-red-700 border-red-200"
                      : "bg-amber-50 text-amber-800 border-amber-200 animate-pulse"
                  )}
                >
                  {approval.status}
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900">
                Action: {approval.action}
              </h3>
            </div>
            <span className="text-xs text-slate-400 font-mono">
              {formatRelativeTime(approval.created_at)}
            </span>
          </div>

          <p className="text-xs text-slate-600 mb-4 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">
            {approval.reason}
          </p>

          {/* Details Preview */}
          <div className="space-y-1.5 text-xs text-slate-600 mb-4">
            <div className="flex justify-between">
              <span className="text-slate-400">Agent:</span>
              <span className="font-semibold text-slate-800">{approval.agent_name || approval.agent_id}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Tool Target:</span>
              <span className="font-mono text-slate-800">{approval.tool_name}</span>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
          <Button
            size="sm"
            variant="ghost"
            onClick={() => setIsDetailOpen(true)}
            leftIcon={<Eye className="w-3.5 h-3.5" />}
          >
            Inspect
          </Button>

          {isPending && (
            <div className="flex items-center gap-2">
              <Button
                size="sm"
                variant="outline"
                onClick={handleReject}
                className="text-red-700 border-red-200 hover:bg-red-50"
                leftIcon={<X className="w-3.5 h-3.5" />}
              >
                Deny
              </Button>
              <Button
                size="sm"
                variant="primary"
                onClick={handleApprove}
                className="bg-emerald-600 hover:bg-emerald-700 text-white"
                leftIcon={<Check className="w-3.5 h-3.5" />}
              >
                Approve
              </Button>
            </div>
          )}

          {!isPending && (
            <span className="text-xs text-slate-400 font-medium">
              Resolved by {approval.resolved_by || "System"}
            </span>
          )}
        </div>
      </div>

      {/* Detail & Parameter Modal */}
      <Modal
        isOpen={isDetailOpen}
        onClose={() => setIsDetailOpen(false)}
        size="lg"
        title={
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-amber-600" />
            <span>Approval Request Details</span>
          </div>
        }
        description={`Ticket ID: ${approval.id} • Risk Level: ${approval.risk_level.toUpperCase()}`}
        footer={
          isPending ? (
            <>
              <Button variant="outline" size="md" onClick={handleReject} className="text-red-700 border-red-200">
                Deny Action
              </Button>
              <Button variant="primary" size="md" onClick={handleApprove} className="bg-emerald-600 hover:bg-emerald-700 text-white">
                Authorize & Execute
              </Button>
            </>
          ) : (
            <Button variant="outline" size="md" onClick={() => setIsDetailOpen(false)}>
              Close
            </Button>
          )
        }
      >
        <div className="space-y-4">
          <div className="p-4 bg-amber-50/60 border border-amber-200/80 rounded-2xl">
            <span className="text-xs font-bold text-amber-900 block mb-1">
              Policy Trigger Reason
            </span>
            <p className="text-xs text-amber-800 leading-relaxed">
              {approval.reason}
            </p>
          </div>

          <div>
            <span className="text-xs font-bold text-slate-800 block mb-1.5">
              Tool Action Request Payload
            </span>
            <pre className="text-xs font-mono bg-slate-900 text-slate-100 p-4 rounded-2xl overflow-x-auto">
              {JSON.stringify(
                {
                  agent: approval.agent_id,
                  tool: approval.tool_name,
                  action: approval.action,
                  parameters: approval.parameters
                },
                null,
                2
              )}
            </pre>
          </div>
        </div>
      </Modal>
    </>
  );
}

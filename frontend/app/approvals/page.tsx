"use client";

import {
  useState
} from "react";

import {
  approveRequest,
  rejectRequest
} from "@/lib/api";


export default function ApprovalCard({
  approval,
  onComplete
}: {
  approval: any;
  onComplete?: () => void;
}) {

  const [loading, setLoading] =
    useState(false);


  async function approve() {

    setLoading(true);

    try {

      await approveRequest(
        approval.id
      );

      onComplete?.();

    } finally {

      setLoading(false);

    }
  }


  async function reject() {

    setLoading(true);

    try {

      await rejectRequest(
        approval.id
      );

      onComplete?.();

    } finally {

      setLoading(false);

    }
  }


  return (

    <div className="rounded-2xl border border-amber-200 bg-white p-6 shadow-sm">

      <div className="flex items-start justify-between">

        <div>

          <p className="text-xs font-semibold uppercase tracking-wider text-amber-600">
            Approval required
          </p>

          <h3 className="mt-2 text-lg font-semibold text-slate-950">
            {approval.agent_id}
          </h3>

        </div>

        <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-700">
          Waiting
        </span>

      </div>


      <div className="mt-5 rounded-xl bg-slate-50 p-4">

        <p className="text-sm text-slate-500">
          Requested action
        </p>

        <p className="mt-1 font-medium text-slate-950">
          {approval.tool_name}
        </p>

      </div>


      <p className="mt-4 text-sm text-slate-600">
        {approval.reason}
      </p>


      <div className="mt-6 flex justify-end gap-3">

        <button
          onClick={reject}
          disabled={loading}
          className="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
        >
          Reject
        </button>

        <button
          onClick={approve}
          disabled={loading}
          className="rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading
            ? "Processing..."
            : "Approve"}
        </button>

      </div>

    </div>
  );
}
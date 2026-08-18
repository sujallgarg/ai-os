"use client";

import React from "react";
import { MemoryItem } from "@/lib/types";
import { getMemoryTypeBadge, formatRelativeTime, cn } from "@/lib/utils";
import { Database, Trash2, Key, Star } from "lucide-react";
import { AIOSClient } from "@/lib/api";

export interface MemoryCardProps {
  memory: MemoryItem;
  onDeleted?: () => void;
}

export function MemoryCard({ memory, onDeleted }: MemoryCardProps) {
  const badge = getMemoryTypeBadge(memory.memory_type);

  const handleDelete = () => {
    if (confirm(`Delete memory key '${memory.key}'?`)) {
      AIOSClient.forgetMemory(memory.key);
      if (onDeleted) onDeleted();
    }
  };

  const isObjectValue = typeof memory.value === "object" && memory.value !== null;

  return (
    <div className="bg-white border border-slate-200/80 hover:border-slate-300 rounded-2xl p-5 shadow-card hover:shadow-elevated transition-all flex flex-col justify-between">
      <div>
        {/* Header */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <div>
            <div className="flex items-center gap-2 mb-1.5 flex-wrap">
              <span className={cn("text-[10px] font-bold px-2 py-0.5 rounded-full border", badge.className)}>
                {badge.label}
              </span>
              <span className="text-[10px] text-slate-400 font-mono">
                Agent: <strong className="text-slate-700">{memory.agent_id}</strong>
              </span>
              <span className="text-[10px] text-amber-600 bg-amber-50 border border-amber-200 px-1.5 py-0.2 rounded font-semibold flex items-center gap-0.5">
                <Star className="w-2.5 h-2.5 fill-amber-500 text-amber-500" /> {memory.importance}/10
              </span>
            </div>
            <div className="flex items-center gap-1.5">
              <Key className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
              <h4 className="text-xs font-bold font-mono text-slate-900 truncate">
                {memory.key}
              </h4>
            </div>
          </div>
          <button
            onClick={handleDelete}
            className="text-slate-400 hover:text-red-600 p-1 rounded-lg hover:bg-red-50 transition-colors"
            title="Forget Memory"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Value Display */}
        <div className="mt-2">
          {isObjectValue ? (
            <pre className="text-[11px] font-mono bg-slate-50 border border-slate-100 text-slate-800 p-3 rounded-xl overflow-x-auto max-h-36">
              {JSON.stringify(memory.value, null, 2)}
            </pre>
          ) : (
            <p className="text-xs text-slate-700 bg-slate-50 border border-slate-100 p-3 rounded-xl leading-relaxed">
              {String(memory.value)}
            </p>
          )}
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400 font-mono">
        <span>Updated {formatRelativeTime(memory.updated_at)}</span>
        {memory.metadata?.source && (
          <span>Source: {memory.metadata.source}</span>
        )}
      </div>
    </div>
  );
}

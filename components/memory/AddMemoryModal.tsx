"use client";

import React, { useState } from "react";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { Button } from "@/components/ui/Button";
import { AIOSClient } from "@/lib/api";
import { Database, Plus } from "lucide-react";
import { MemoryType } from "@/lib/types";

export interface AddMemoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAdded?: () => void;
}

export function AddMemoryModal({ isOpen, onClose, onAdded }: AddMemoryModalProps) {
  const [key, setKey] = useState("");
  const [value, setValue] = useState("");
  const [agentId, setAgentId] = useState("supervisor");
  const [memoryType, setMemoryType] = useState<MemoryType>("shared");
  const [importance, setImportance] = useState(5);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!key.trim() || !value.trim()) return;

    let parsedValue: any = value.trim();
    try {
      if (value.trim().startsWith("{") || value.trim().startsWith("[")) {
        parsedValue = JSON.parse(value.trim());
      }
    } catch {
      // Keep as string
    }

    AIOSClient.addMemory({
      key: key.trim(),
      value: parsedValue,
      agent_id: agentId,
      memory_type: memoryType,
      importance: Number(importance),
    });

    setKey("");
    setValue("");
    onClose();
    if (onAdded) onAdded();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size="md"
      title={
        <div className="flex items-center gap-2">
          <Database className="w-5 h-5 text-indigo-600" />
          <span>Write Shared Agent Memory</span>
        </div>
      }
      description="Store persistent facts, user preferences, configurations, or knowledge items."
      footer={
        <>
          <Button variant="ghost" size="md" onClick={onClose}>
            Cancel
          </Button>
          <Button
            variant="primary"
            size="md"
            onClick={handleSubmit}
            disabled={!key.trim() || !value.trim()}
          >
            Save Memory Key
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            Memory Key (dot-separated) <span className="text-red-500">*</span>
          </label>
          <Input
            value={key}
            onChange={(e) => setKey(e.target.value)}
            placeholder="e.g. client.theme or user.company_name"
            autoFocus
          />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <Select
              label="Memory Type"
              value={memoryType}
              onChange={(e) => setMemoryType(e.target.value as MemoryType)}
              options={[
                { value: "shared", label: "Shared (Global)" },
                { value: "preference", label: "User Preference" },
                { value: "goal", label: "Goal Objective" },
                { value: "task", label: "Task Context" },
                { value: "result", label: "Execution Result" },
                { value: "private", label: "Agent Private" },
              ]}
            />
          </div>
          <div>
            <Select
              label="Owning Agent"
              value={agentId}
              onChange={(e) => setAgentId(e.target.value)}
              options={[
                { value: "supervisor", label: "Supervisor Agent" },
                { value: "email", label: "Email Agent" },
                { value: "coding", label: "Coding Agent" },
                { value: "browser", label: "Browser Agent" },
                { value: "calendar", label: "Calendar Agent" },
                { value: "file", label: "File Agent" },
              ]}
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            Importance Level (1-10): <strong className="text-slate-900 font-mono">{importance}</strong>
          </label>
          <input
            type="range"
            min={1}
            max={10}
            value={importance}
            onChange={(e) => setImportance(Number(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            Value / JSON Content <span className="text-red-500">*</span>
          </label>
          <textarea
            rows={4}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder='e.g. "dark" or {"theme": "light", "apiKey": "xyz"}'
            className="w-full bg-white border border-slate-200 rounded-xl p-3 text-xs font-mono text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-500/10 resize-none"
          />
        </div>
      </form>
    </Modal>
  );
}

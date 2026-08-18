"use client";

import React, { useState } from "react";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { Button } from "@/components/ui/Button";
import { AIOSClient } from "@/lib/api";
import { CalendarClock } from "lucide-react";

export interface CreateScheduleModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated?: () => void;
}

export function CreateScheduleModal({ isOpen, onClose, onCreated }: CreateScheduleModalProps) {
  const [name, setName] = useState("");
  const [prompt, setPrompt] = useState("");
  const [cron, setCron] = useState("0 8 * * 1-5 (Weekdays at 8:00 AM)");
  const [agent, setAgent] = useState("supervisor");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !prompt.trim()) return;

    AIOSClient.addSchedule({
      name: name.trim(),
      goal_prompt: prompt.trim(),
      cron_or_interval: cron,
      run_at: new Date(Date.now() + 1000 * 60 * 60 * 12).toISOString(),
      next_run: new Date(Date.now() + 1000 * 60 * 60 * 12).toISOString(),
      recurring: true,
      interval_seconds: 86400,
      enabled: true,
      target_agent: agent,
    });

    setName("");
    setPrompt("");
    onClose();
    if (onCreated) onCreated();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size="md"
      title={
        <div className="flex items-center gap-2">
          <CalendarClock className="w-5 h-5 text-primary-600" />
          <span>Create Scheduled Task</span>
        </div>
      }
      description="Configure recurring or delayed autonomous execution triggers."
      footer={
        <>
          <Button variant="ghost" size="md" onClick={onClose}>
            Cancel
          </Button>
          <Button
            variant="primary"
            size="md"
            onClick={handleSubmit}
            disabled={!name.trim() || !prompt.trim()}
          >
            Create Schedule
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            Schedule Name <span className="text-red-500">*</span>
          </label>
          <Input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. Daily Morning Inbox Triage"
            autoFocus
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            Autonomous Goal Prompt <span className="text-red-500">*</span>
          </label>
          <textarea
            rows={3}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g. Check Gmail for urgent client messages and draft concise bullet-point summary..."
            className="w-full bg-white border border-slate-200 rounded-xl p-3 text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-500/10 resize-none"
          />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <Select
              label="Cadence / Interval"
              value={cron}
              onChange={(e) => setCron(e.target.value)}
              options={[
                { value: "0 8 * * 1-5 (Weekdays at 8:00 AM)", label: "Weekdays (8:00 AM)" },
                { value: "0 2 * * * (Daily at 2:00 AM)", label: "Daily (2:00 AM)" },
                { value: "0 * * * * (Hourly)", label: "Hourly" },
                { value: "0 9 * * 1 (Every Monday)", label: "Weekly (Monday)" },
              ]}
            />
          </div>
          <div>
            <Select
              label="Primary Target Agent"
              value={agent}
              onChange={(e) => setAgent(e.target.value)}
              options={[
                { value: "supervisor", label: "Supervisor Agent" },
                { value: "email", label: "Email Agent" },
                { value: "coding", label: "Coding Agent" },
                { value: "browser", label: "Browser Agent" },
                { value: "file", label: "File Agent" },
              ]}
            />
          </div>
        </div>
      </form>
    </Modal>
  );
}

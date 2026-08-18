"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { AIOSClient } from "@/lib/api";
import { Sparkles, Bot, ArrowRight, ShieldCheck, Zap } from "lucide-react";

export interface GoalCreationModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const PRESET_GOALS = [
  {
    title: "Build and test a SaaS Landing Page with Tailwind & React",
    description: "Decomposes into requirements analysis, code scaffolding, testimonial integration, and Playwright viewport testing.",
    icon: Zap,
    tag: "Coding + Browser",
  },
  {
    title: "Check Gmail for partner proposals and draft executive replies",
    description: "Searches unread client emails, extracts key terms, drafts tailored responses, and requests human confirmation before dispatch.",
    icon: Bot,
    tag: "Email + Approvals",
  },
  {
    title: "Research competitor pricing models and generate PDF report",
    description: "Launches headless browser across 5 target catalogs, normalizes token costs, stores in memory, and writes analysis document.",
    icon: Sparkles,
    tag: "Browser + Intelligence",
  },
  {
    title: "Database snapshot backup and encryption verification",
    description: "Creates backup of shared memory database, generates AES-256 integrity hash, and archives to cloud storage.",
    icon: ShieldCheck,
    tag: "Storage + Security",
  },
];

export function GoalCreationModal({ isOpen, onClose }: GoalCreationModalProps) {
  const router = useRouter();
  const [goalText, setGoalText] = useState("");
  const [description, setDescription] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!goalText.trim()) return;

    setIsSubmitting(true);
    try {
      const newGoal = AIOSClient.createGoal(goalText.trim(), description.trim() || undefined);
      setGoalText("");
      setDescription("");
      setIsSubmitting(false);
      onClose();
      router.push(`/goals/${newGoal.id}`);
    } catch (err) {
      console.error("Failed to create goal:", err);
      setIsSubmitting(false);
    }
  };

  const handleSelectPreset = (preset: (typeof PRESET_GOALS)[0]) => {
    setGoalText(preset.title);
    setDescription(preset.description);
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size="lg"
      title={
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-primary-50 text-primary-600 flex items-center justify-center">
            <Sparkles className="w-4 h-4" />
          </div>
          <span>Dispatch Autonomous Goal</span>
        </div>
      }
      description="The Planner will analyze your objective, generate an execution DAG, and coordinate the Agent Swarm."
      footer={
        <>
          <Button variant="ghost" size="md" onClick={onClose} disabled={isSubmitting}>
            Cancel
          </Button>
          <Button
            variant="primary"
            size="md"
            onClick={() => handleSubmit()}
            disabled={!goalText.trim() || isSubmitting}
            isLoading={isSubmitting}
            rightIcon={<ArrowRight className="w-4 h-4" />}
          >
            Plan & Execute
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            What is your objective? <span className="text-red-500">*</span>
          </label>
          <textarea
            rows={2}
            value={goalText}
            onChange={(e) => setGoalText(e.target.value)}
            placeholder="e.g. Build and deploy a client portal with authentication and email notifications"
            className="w-full bg-white border border-slate-200 rounded-xl p-3 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-500/10 transition-all resize-none"
            autoFocus
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            Additional Context or Constraints (Optional)
          </label>
          <Input
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="e.g. Target production environment, require approvals for outbound emails"
          />
        </div>

        {/* Preset Templates */}
        <div className="pt-2">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-2">
            Suggested Autonomous Objectives
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {PRESET_GOALS.map((preset, idx) => {
              const Icon = preset.icon;
              return (
                <button
                  type="button"
                  key={idx}
                  onClick={() => handleSelectPreset(preset)}
                  className="text-left p-3 rounded-xl border border-slate-200/80 hover:border-primary-300 hover:bg-primary-50/30 transition-all duration-150 group flex flex-col justify-between"
                >
                  <div className="flex items-start gap-2 mb-1.5">
                    <Icon className="w-4 h-4 text-slate-400 group-hover:text-primary-600 mt-0.5 flex-shrink-0" />
                    <span className="text-xs font-semibold text-slate-800 group-hover:text-primary-900 leading-snug line-clamp-2">
                      {preset.title}
                    </span>
                  </div>
                  <span className="text-[10px] font-medium text-slate-400 bg-slate-100 group-hover:bg-primary-100/70 group-hover:text-primary-700 px-1.5 py-0.5 rounded self-start">
                    {preset.tag}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </form>
    </Modal>
  );
}

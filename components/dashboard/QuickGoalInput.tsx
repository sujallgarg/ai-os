"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { AIOSClient } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Sparkles, ArrowRight, CornerDownLeft } from "lucide-react";

export function QuickGoalInput() {
  const router = useRouter();
  const [goalText, setGoalText] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!goalText.trim()) return;

    setIsSubmitting(true);
    try {
      const newGoal = AIOSClient.createGoal(goalText.trim());
      setGoalText("");
      setIsSubmitting(false);
      router.push(`/goals/${newGoal.id}`);
    } catch (err) {
      console.error(err);
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/90 shadow-elevated transition-all">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-6 h-6 rounded-lg bg-primary-50 text-primary-600 flex items-center justify-center">
          <Sparkles className="w-3.5 h-3.5" />
        </div>
        <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
          Autonomous Operating System Dispatcher
        </span>
      </div>

      <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight mb-2">
        What objective would you like the Agent Swarm to execute?
      </h2>
      <p className="text-xs sm:text-sm text-slate-500 mb-5 max-w-2xl leading-relaxed">
        Describe any multi-step goal. The planner will generate a dependency DAG, select optimal agent capabilities, and orchestrate execution.
      </p>

      <form onSubmit={handleSubmit} className="relative">
        <div className="relative flex items-center">
          <input
            type="text"
            value={goalText}
            onChange={(e) => setGoalText(e.target.value)}
            placeholder="e.g. Build and test a SaaS landing page for my product..."
            className="w-full bg-slate-50/70 border border-slate-200/90 rounded-2xl px-5 py-4 text-sm sm:text-base text-slate-900 placeholder:text-slate-400 focus:outline-none focus:bg-white focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all shadow-subtle pr-32"
          />
          <div className="absolute right-2.5 flex items-center gap-2">
            <Button
              type="submit"
              variant="primary"
              size="md"
              disabled={!goalText.trim() || isSubmitting}
              isLoading={isSubmitting}
              rightIcon={<ArrowRight className="w-4 h-4" />}
              className="rounded-xl shadow-sm"
            >
              Dispatch
            </Button>
          </div>
        </div>
      </form>

      {/* Suggested Quick Prompts */}
      <div className="flex items-center gap-2 mt-4 flex-wrap text-xs text-slate-500">
        <span className="font-semibold text-slate-400">Try:</span>
        {[
          "Build and test landing page",
          "Triage unread Gmail threads & draft replies",
          "Scrape competitor pricing models",
          "Snapshot memory database backup"
        ].map((prompt) => (
          <button
            key={prompt}
            type="button"
            onClick={() => setGoalText(prompt)}
            className="px-2.5 py-1 rounded-lg bg-slate-100/70 hover:bg-slate-200/60 hover:text-slate-800 text-slate-600 transition-colors font-medium text-[11px]"
          >
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
}

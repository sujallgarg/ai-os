"use client";

import React, { useEffect, useState } from "react";
import { AIOSClient } from "@/lib/api";
import { Goal } from "@/lib/types";
import { GoalCard } from "@/components/goals/GoalCard";
import { Button } from "@/components/ui/Button";
import { Tabs } from "@/components/ui/Tabs";
import { GoalCreationModal } from "@/components/goals/GoalCreationModal";
import { Target, Plus, Search, Filter } from "lucide-react";

export default function GoalsPage() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [activeTab, setActiveTab] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  const refreshGoals = () => {
    setGoals(AIOSClient.getGoals());
  };

  useEffect(() => {
    refreshGoals();
    const interval = setInterval(refreshGoals, 3000);
    return () => clearInterval(interval);
  }, []);

  const inProgressCount = goals.filter((g) => g.status === "in_progress").length;
  const completedCount = goals.filter((g) => g.status === "completed").length;
  const queuedCount = goals.filter((g) => g.status === "queued").length;

  const filteredGoals = goals.filter((g) => {
    const matchesSearch =
      g.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      g.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      g.tags.some((t) => t.toLowerCase().includes(searchQuery.toLowerCase()));

    if (activeTab === "in_progress") return matchesSearch && g.status === "in_progress";
    if (activeTab === "completed") return matchesSearch && g.status === "completed";
    if (activeTab === "queued") return matchesSearch && g.status === "queued";
    return matchesSearch;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Autonomous Goals
            </h1>
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
              {goals.length} Goals Total
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 max-w-xl">
            Objectives broken down by the Planner into dependency graphs and executed autonomously.
          </p>
        </div>

        <Button
          variant="primary"
          size="md"
          onClick={() => setIsModalOpen(true)}
          leftIcon={<Plus className="w-4 h-4" />}
          className="shadow-sm"
        >
          New Goal
        </Button>
      </div>

      {/* Filter Tabs & Search Bar */}
      <div className="flex items-center justify-between gap-4 flex-wrap pb-2 border-b border-slate-200/80">
        <Tabs
          tabs={[
            { id: "all", label: "All Goals", count: goals.length },
            { id: "in_progress", label: "In Progress", count: inProgressCount },
            { id: "completed", label: "Completed", count: completedCount },
            { id: "queued", label: "Queued", count: queuedCount },
          ]}
          activeTab={activeTab}
          onChange={setActiveTab}
          className="border-b-0"
        />

        <div className="relative min-w-[240px]">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search goals by keyword or tag..."
            className="w-full bg-white border border-slate-200 rounded-xl pl-9 pr-3.5 py-1.5 text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-500/10"
          />
        </div>
      </div>

      {/* Goals Grid */}
      {filteredGoals.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 text-xs text-slate-400">
          No goals found matching your search.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredGoals.map((goal) => (
            <GoalCard key={goal.id} goal={goal} />
          ))}
        </div>
      )}

      {/* Creation Modal */}
      <GoalCreationModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          refreshGoals();
        }}
      />
    </div>
  );
}

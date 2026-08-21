"use client";

import React, { useEffect, useState } from "react";
import { AIOSClient } from "@/lib/api";
import { MemoryItem, MemoryType } from "@/lib/types";
import { MemoryCard } from "@/components/memory/MemoryCard";
import { AddMemoryModal } from "@/components/memory/AddMemoryModal";
import { Button } from "@/components/ui/Button";
import { Tabs } from "@/components/ui/Tabs";
import { Database, Plus, Search } from "lucide-react";

export default function MemoryPage() {
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [activeTab, setActiveTab] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  const refreshMemories = () => {
    setMemories(AIOSClient.getMemories());
  };

  useEffect(() => {
    refreshMemories();
  }, []);

  const filteredMemories = memories.filter((m) => {
    const matchesSearch =
      m.key.toLowerCase().includes(searchQuery.toLowerCase()) ||
      JSON.stringify(m.value).toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.agent_id.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesType = activeTab === "all" || m.memory_type === activeTab;
    return matchesSearch && matchesType;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Shared Agent Memory
            </h1>
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200">
              {memories.length} Knowledge Keys
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 max-w-xl">
            Persistent cross-agent knowledge repository holding user preferences, synthesized task outputs, benchmark telemetry, and environmental state.
          </p>
        </div>

        <Button
          variant="primary"
          size="md"
          onClick={() => setIsModalOpen(true)}
          leftIcon={<Plus className="w-4 h-4" />}
          className="shadow-sm"
        >
          Write Memory
        </Button>
      </div>

      {/* Tabs & Search */}
      <div className="flex items-center justify-between gap-4 flex-wrap pb-2 border-b border-slate-200/80">
        <Tabs
          tabs={[
            { id: "all", label: "All Types", count: memories.length },
            { id: "preference", label: "Preferences" },
            { id: "shared", label: "Shared" },
            { id: "result", label: "Results" },
            { id: "goal", label: "Goals" },
            { id: "private", label: "Private" },
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
            placeholder="Search keys or values..."
            className="w-full bg-white border border-slate-200 rounded-xl pl-9 pr-3.5 py-1.5 text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-500/10"
          />
        </div>
      </div>

      {/* Memory Grid */}
      {filteredMemories.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 text-xs text-slate-400">
          No memory entries found matching your query.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredMemories.map((mem) => (
            <MemoryCard key={mem.key} memory={mem} onDeleted={refreshMemories} />
          ))}
        </div>
      )}

      {/* Write Memory Modal */}
      <AddMemoryModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onAdded={refreshMemories}
      />
    </div>
  );
}

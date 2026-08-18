"use client";

import React, { useEffect, useState } from "react";
import { AIOSClient } from "@/lib/api";
import { ScheduledTask } from "@/lib/types";
import { ScheduleCard } from "@/components/schedules/ScheduleCard";
import { CreateScheduleModal } from "@/components/schedules/CreateScheduleModal";
import { Button } from "@/components/ui/Button";
import { CalendarClock, Plus } from "lucide-react";

export default function SchedulesPage() {
  const [schedules, setSchedules] = useState<ScheduledTask[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const refreshSchedules = () => {
    setSchedules(AIOSClient.getSchedules());
  };

  useEffect(() => {
    refreshSchedules();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Task Schedules & Cron Triggers
            </h1>
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
              {schedules.filter((s) => s.enabled).length} Active Crons
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 max-w-xl">
            Automated recurring triggers that dispatch autonomous goals at specified cadences (daily triage, hourly backups, weekly intelligence scans).
          </p>
        </div>

        <Button
          variant="primary"
          size="md"
          onClick={() => setIsModalOpen(true)}
          leftIcon={<Plus className="w-4 h-4" />}
          className="shadow-sm"
        >
          New Schedule
        </Button>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {schedules.map((schedule) => (
          <ScheduleCard
            key={schedule.id}
            schedule={schedule}
            onToggled={refreshSchedules}
            onRunNow={refreshSchedules}
          />
        ))}
      </div>

      {/* Modal */}
      <CreateScheduleModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCreated={refreshSchedules}
      />
    </div>
  );
}

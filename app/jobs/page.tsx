"use client";

import React, { useEffect, useState } from "react";
import { AIOSClient } from "@/lib/api";
import { Job } from "@/lib/types";
import { JobCard } from "@/components/jobs/JobCard";
import { Button } from "@/components/ui/Button";
import { Cpu, Plus } from "lucide-react";

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);

  const fetchJobs = () => {
    setJobs(AIOSClient.getJobs());
  };

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Background Jobs & Batch Runner
            </h1>
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
              {jobs.filter((j) => j.status === "running").length} Running
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 max-w-xl">
            Long-running background processes, parallel batch pipelines, and asynchronous agent telemetry logs.
          </p>
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {jobs.map((job) => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>
    </div>
  );
}

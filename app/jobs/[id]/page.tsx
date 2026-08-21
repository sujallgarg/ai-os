"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import LiveActivity from "@/components/LiveActivity";
import { useRealtime } from "@/hooks/useRealtime";
import { getJob } from "@/lib/api";
import {
  CheckCircle2,
  Clock,
  ShieldAlert,
  Sparkles,
  Bot,
  ArrowRight,
  ArrowLeft,
  Mail,
  Search,
  FileText,
  ShieldCheck
} from "lucide-react";

interface Job {
  id: string;
  goal: string;
  status: string;
  progress: number;
  result?: any;
  error?: string | null;
}

export default function JobDetailPage({
  params
}: {
  params: Promise<{ id: string }> | { id: string }
}) {
  const [job, setJob] = useState<Job | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);

  const { events, isConnected } = useRealtime(jobId || undefined);

  useEffect(() => {
    Promise.resolve(params).then((p) => {
      if (p?.id) {
        setJobId(p.id);
      }
    });
  }, [params]);

  useEffect(() => {
    if (!jobId) return;

    let active = true;
    const currentId = jobId;

    async function load() {
      try {
        const data = await getJob(currentId);
        if (active && data) {
          setJob(data as Job);
        }
      } catch (error) {
        console.error(error);
      }
    }

    load();
    const interval = setInterval(load, 2000);
    return () => {
      active = false;
      clearInterval(interval);
    };
  }, [jobId]);

  if (!job) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Sidebar />
        <div className="lg:pl-64">
          <Topbar />
          <main className="flex min-h-[60vh] items-center justify-center p-6">
            <div className="flex items-center gap-3 text-sm text-slate-500">
              <span className="h-2 w-2 rounded-full bg-indigo-600 animate-ping" />
              Loading live job telemetry...
            </div>
          </main>
        </div>
      </div>
    );
  }

  const progress = job.progress || 0;

  // Determine stage statuses based on progress
  const stages = [
    {
      title: "Goal Received",
      agent: "Planner Agent",
      icon: Sparkles,
      description: "Deconstructed objective & generated task graph",
      done: progress >= 10,
      active: progress > 0 && progress < 25
    },
    {
      title: "Context Gathering",
      agent: "Email / Research Agent",
      icon: Mail,
      description: "Scanning Gmail inbox & retrieving thread history",
      done: progress >= 40,
      active: progress >= 25 && progress < 60
    },
    {
      title: "Analysis & Drafting",
      agent: "Executive Agent",
      icon: FileText,
      description: "Synthesizing information & drafting replies",
      done: progress >= 75,
      active: progress >= 60 && progress < 85
    },
    {
      title: "Policy & Execution",
      agent: "Security Engine",
      icon: ShieldCheck,
      description: "Passing policy check & requesting human authorization",
      done: progress >= 100,
      active: progress >= 85
    }
  ];

  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />

      <div className="lg:pl-64">
        <Topbar />

        <main className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8 space-y-8">
          {/* Back to Dashboard */}
          <div>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-slate-900 transition"
            >
              <ArrowLeft size={16} />
              Back to Command Center
            </Link>
          </div>

          {/* Job Overview Header Card */}
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-6">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold uppercase tracking-wider text-indigo-600">
                    Autonomous Job Stream
                  </span>
                  <span className="h-1.5 w-1.5 rounded-full bg-slate-300" />
                  <span className="font-mono text-xs text-slate-400">
                    {job.id}
                  </span>
                </div>

                <h1 className="mt-3 text-2xl font-bold tracking-tight text-slate-950">
                  {job.goal}
                </h1>
              </div>

              <div className="flex items-center gap-2">
                <span className="relative flex h-2.5 w-2.5">
                  {job.status === "running" && (
                    <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-indigo-400 opacity-75" />
                  )}
                  <span
                    className={`relative inline-flex h-2.5 w-2.5 rounded-full ${
                      job.status === "completed"
                        ? "bg-emerald-500"
                        : job.status === "failed"
                        ? "bg-red-500"
                        : "bg-indigo-600"
                    }`}
                  />
                </span>

                <span
                  className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide ${
                    job.status === "completed"
                      ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                      : job.status === "failed"
                      ? "bg-red-50 text-red-700 border border-red-200"
                      : "bg-indigo-50 text-indigo-700 border border-indigo-200"
                  }`}
                >
                  {job.status}
                </span>
              </div>
            </div>

            {/* Overall Progress Bar */}
            <div className="mt-8">
              <div className="mb-2 flex justify-between text-sm">
                <span className="font-medium text-slate-500">Autonomous Execution Progress</span>
                <span className="font-bold text-slate-950">{progress}%</span>
              </div>

              <div className="h-3 overflow-hidden rounded-full bg-slate-100 p-0.5">
                <div
                  className="h-full rounded-full bg-indigo-600 transition-all duration-700 shadow-sm"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>

            {job.status === "completed" && (
              <div className="mt-8 rounded-2xl bg-emerald-50/80 border border-emerald-100 p-5">
                <div className="flex items-center gap-3 text-emerald-800 font-semibold">
                  <CheckCircle2 size={18} className="text-emerald-600" />
                  Goal Fully Executed
                </div>
                <p className="mt-1 text-sm text-emerald-700">
                  Your autonomous AI team completed all tasks in the execution DAG cleanly.
                </p>
              </div>
            )}

            {job.status === "failed" && (
              <div className="mt-8 rounded-2xl bg-red-50/80 border border-red-100 p-5">
                <div className="flex items-center gap-3 text-red-800 font-semibold">
                  <ShieldAlert size={18} className="text-red-600" />
                  Execution Failed
                </div>
                <p className="mt-1 text-sm text-red-700">{job.error || "Task dependency failed."}</p>
              </div>
            )}
          </div>

          {/* Section 1: Visual Task Graph Pipeline */}
          <section className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold tracking-tight text-slate-950">
                Agent Pipeline & Task Graph
              </h2>
              <span className="text-xs text-slate-500 font-medium">4 Autonomous Stages</span>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {stages.map((st, idx) => {
                const Icon = st.icon;
                return (
                  <div
                    key={st.title}
                    className={`relative rounded-2xl border p-5 transition-all duration-300 ${
                      st.done
                        ? "border-emerald-200 bg-emerald-50/30"
                        : st.active
                        ? "border-indigo-300 bg-indigo-50/40 ring-2 ring-indigo-100"
                        : "border-slate-200 bg-white opacity-70"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div
                        className={`flex h-9 w-9 items-center justify-center rounded-xl font-bold text-xs ${
                          st.done
                            ? "bg-emerald-600 text-white"
                            : st.active
                            ? "bg-indigo-600 text-white animate-pulse"
                            : "bg-slate-100 text-slate-500"
                        }`}
                      >
                        {st.done ? <CheckCircle2 size={16} /> : idx + 1}
                      </div>

                      <Icon
                        size={18}
                        className={
                          st.done
                            ? "text-emerald-600"
                            : st.active
                            ? "text-indigo-600"
                            : "text-slate-400"
                        }
                      />
                    </div>

                    <h3 className="mt-4 font-semibold text-slate-950 text-sm">
                      {st.title}
                    </h3>
                    <p className="mt-0.5 text-xs text-indigo-700 font-medium">
                      {st.agent}
                    </p>
                    <p className="mt-2 text-xs text-slate-500 leading-relaxed">
                      {st.description}
                    </p>
                  </div>
                );
              })}
            </div>
          </section>

          {/* Section 2: Step-by-Step Live Execution Timeline */}
          <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm space-y-6">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div>
                <h2 className="text-lg font-bold tracking-tight text-slate-950">
                  Execution Timeline & Activity
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Human-readable step activity and agent telemetry
                </p>
              </div>

              <div className="flex items-center gap-2 text-xs font-semibold text-indigo-600 bg-indigo-50 px-3 py-1.5 rounded-full">
                <span className="h-2 w-2 rounded-full bg-indigo-600 animate-pulse" />
                Live Updating
              </div>
            </div>

            {/* Timeline Stream */}
            <div className="space-y-4 relative before:absolute before:left-3.5 before:top-3 before:bottom-3 before:w-0.5 before:bg-slate-100">
              {/* Event 1: Goal Decomposition */}
              <div className="flex gap-4 items-start relative z-10">
                <div className="flex h-7 w-7 items-center justify-center rounded-full bg-emerald-600 text-white text-xs font-bold shadow-sm">
                  ✓
                </div>
                <div className="flex-1 rounded-2xl border border-slate-100 bg-slate-50 p-4">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-semibold text-slate-950">
                      Goal Understood & Plan Created
                    </p>
                    <span className="text-[11px] font-medium text-slate-400">Completed</span>
                  </div>
                  <p className="mt-1 text-xs text-slate-600">
                    MultiAgentPlanner generated execution DAG with task dependencies.
                  </p>
                </div>
              </div>

              {/* Event 2: Agent Working / Context Search */}
              <div className="flex gap-4 items-start relative z-10">
                <div
                  className={`flex h-7 w-7 items-center justify-center rounded-full font-bold text-xs shadow-sm ${
                    progress >= 40
                      ? "bg-emerald-600 text-white"
                      : "bg-indigo-600 text-white animate-bounce"
                  }`}
                >
                  {progress >= 40 ? "✓" : "◉"}
                </div>
                <div className="flex-1 rounded-2xl border border-indigo-100 bg-indigo-50/50 p-4">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-semibold text-slate-950 flex items-center gap-2">
                      <Bot size={15} className="text-indigo-600" />
                      Email Agent Scanning Gmail Inbox
                    </p>
                    <span className="text-[11px] font-semibold text-indigo-700">
                      {progress >= 40 ? "Completed" : "Active Stage"}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-slate-600">
                    Executing tool operation <code className="bg-indigo-100/70 px-1.5 py-0.5 rounded text-indigo-800 font-mono text-[11px]">gmail.search</code> for query "partner proposals".
                  </p>
                </div>
              </div>

              {/* Event 3: Analysis & Reply Drafting */}
              <div className="flex gap-4 items-start relative z-10">
                <div
                  className={`flex h-7 w-7 items-center justify-center rounded-full font-bold text-xs shadow-sm ${
                    progress >= 75
                      ? "bg-emerald-600 text-white"
                      : progress >= 40
                      ? "bg-indigo-600 text-white animate-pulse"
                      : "bg-slate-200 text-slate-500"
                  }`}
                >
                  {progress >= 75 ? "✓" : progress >= 40 ? "◉" : "○"}
                </div>
                <div className="flex-1 rounded-2xl border border-slate-100 bg-slate-50 p-4">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-semibold text-slate-950">
                      Executive Reply Drafting
                    </p>
                    <span className="text-[11px] font-medium text-slate-400">
                      {progress >= 75 ? "Completed" : "Queued"}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-slate-600">
                    Formatting executive reply context with tone-preserved AI writing.
                  </p>
                </div>
              </div>

              {/* Event 4: Human Authorization Gate */}
              <div className="flex gap-4 items-start relative z-10">
                <div
                  className={`flex h-7 w-7 items-center justify-center rounded-full font-bold text-xs shadow-sm ${
                    progress >= 100
                      ? "bg-emerald-600 text-white"
                      : "bg-slate-200 text-slate-500"
                  }`}
                >
                  {progress >= 100 ? "✓" : "○"}
                </div>
                <div className="flex-1 rounded-2xl border border-slate-100 bg-slate-50 p-4">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-semibold text-slate-950 flex items-center gap-2">
                      <ShieldAlert size={15} className="text-amber-500" />
                      Policy Check & Human Approval Gate
                    </p>
                    <span className="text-[11px] font-medium text-slate-400">
                      {progress >= 100 ? "Authorized" : "Pending Gate"}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-slate-600">
                    High-risk action <code className="bg-slate-200/70 px-1.5 py-0.5 rounded text-slate-800 font-mono text-[11px]">gmail.send</code> requires human sign-off before dispatching emails.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Section 3: Live Telemetry Event Log Stream */}
          {events.length > 0 && (
            <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm space-y-4">
              <h2 className="text-sm font-bold uppercase tracking-wider text-indigo-600">
                Real-Time Telemetry Stream
              </h2>
              <div className="space-y-2 max-h-48 overflow-y-auto pr-2">
                {events.map((evt, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-3 rounded-xl bg-slate-50 text-xs font-mono text-slate-700 border border-slate-100"
                  >
                    <div className="flex items-center gap-2">
                      <span className="h-1.5 w-1.5 rounded-full bg-indigo-600" />
                      <span>{evt.event}</span>
                    </div>
                    <span className="text-slate-400">
                      {evt.data?.metadata?.description || evt.data?.message || "Event recorded"}
                    </span>
                  </div>
                ))}
              </div>
            </section>
          )}
        </main>
      </div>

      {/* Floating Live AI Activity Window */}
      <LiveActivity jobId={jobId || undefined} />
    </div>
  );
}

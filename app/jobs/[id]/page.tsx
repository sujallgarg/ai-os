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
  ArrowLeft,
  Mail,
  FileText,
  ShieldCheck,
  Send,
  Inbox,
  FileEdit,
  Eye
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
  const [selectedMail, setSelectedMail] = useState<any | null>(null);

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

  // Extract Email Agent Activity Artifacts
  const emailActivity = job.result?.email_activity || {};
  const readEmails: any[] = emailActivity.read_emails || [
    {
      id: "msg_001",
      from: "Alex Rivera <alex.rivera@partnerorg.com>",
      subject: "Strategic Partnership & Executive Integration Proposal",
      snippet: "Hi Team, we reviewed your AI platform and would love to explore a joint executive integration. Attached is our proposal...",
      date: "Today, 2:15 PM"
    },
    {
      id: "msg_002",
      from: "Sarah Chen <sarah@enterprise-saas.io>",
      subject: "Enterprise SaaS License Expansion Query",
      snippet: "Hello, we are looking to deploy 50 autonomous agent seats across our product engineering group...",
      date: "Today, 11:30 AM"
    }
  ];

  const drafts: any[] = emailActivity.generated_drafts || [
    {
      to: "Alex Rivera <alex.rivera@partnerorg.com>",
      subject: "Re: Strategic Partnership & Executive Integration Proposal",
      body: "Hi Alex,\n\nThank you for reaching out regarding the strategic partnership proposal. Our executive AI team has reviewed the terms and we are excited to integrate.\n\nBest regards,\nExecutive AI Agent"
    }
  ];

  const approvalTickets: any[] = emailActivity.approval_tickets || [];

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
      title: "Reading Inbox & Threads",
      agent: "Email Agent (`gmail.read`)",
      icon: Mail,
      description: "Scanning Gmail inbox & retrieving thread messages",
      done: progress >= 40,
      active: progress >= 25 && progress < 60
    },
    {
      title: "Analysis & AI Drafting",
      agent: "Executive Agent (`gmail.draft`)",
      icon: FileText,
      description: "Synthesizing email context & generating draft reply",
      done: progress >= 75,
      active: progress >= 60 && progress < 85
    },
    {
      title: "Policy & Human Authorization",
      agent: "Security Engine (`gmail.send`)",
      icon: ShieldCheck,
      description: "Evaluating security policies & issuing approval ticket",
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

          {/* Section 2: Detailed Email Agent Artifacts (Emails Read & Drafts Generated) */}
          <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm space-y-6">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-600 flex items-center gap-1.5">
                  <Mail size={15} /> Email Agent Workstation Outputs
                </span>
                <h2 className="text-xl font-bold tracking-tight text-slate-950 mt-1">
                  Emails Read, AI Drafts & Authorization Gates
                </h2>
              </div>
              <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full">
                Full Agent Trace Active
              </span>
            </div>

            {/* Sub-section A: Emails Read by Agent */}
            <div className="space-y-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-2">
                <Inbox size={14} className="text-indigo-600" />
                1. Emails Read by Agent (`gmail.read` / `gmail.search`)
              </h3>

              <div className="grid gap-3 sm:grid-cols-2">
                {readEmails.map((mail, idx) => (
                  <div
                    key={idx}
                    onClick={() => setSelectedMail(mail)}
                    className="cursor-pointer rounded-2xl border border-slate-200 bg-slate-50 p-4 hover:border-indigo-300 hover:bg-indigo-50/30 transition space-y-2"
                  >
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-900 truncate max-w-[200px]">{mail.from}</span>
                      <span className="text-[10px] text-slate-400">{mail.date || "Today"}</span>
                    </div>
                    <p className="text-xs font-semibold text-indigo-950 truncate">{mail.subject}</p>
                    <p className="text-xs text-slate-500 line-clamp-2">{mail.snippet}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Sub-section B: AI Reply Draft Created */}
            <div className="space-y-3 pt-4 border-t border-slate-100">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-2">
                <FileEdit size={14} className="text-indigo-600" />
                2. AI Response Draft Created (`gmail.draft` / `draft_reply`)
              </h3>

              {drafts.map((d, idx) => (
                <div key={idx} className="rounded-2xl border border-indigo-200 bg-indigo-50/40 p-5 space-y-3">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-indigo-950">To: {d.to || "Recipient"}</span>
                    <span className="text-[11px] font-semibold text-emerald-700 bg-white border border-emerald-200 px-2.5 py-0.5 rounded-full">
                      AI Draft Ready
                    </span>
                  </div>

                  <p className="text-xs font-semibold text-slate-900">Subject: {d.subject || "Executive Response"}</p>

                  <pre className="text-xs text-slate-700 font-sans whitespace-pre-wrap leading-relaxed bg-white p-4 rounded-xl border border-indigo-100">
                    {typeof d.body === "string" ? d.body : typeof d === "string" ? d : JSON.stringify(d)}
                  </pre>
                </div>
              ))}
            </div>

            {/* Sub-section C: Human Send Approval Request Gate */}
            <div className="space-y-3 pt-4 border-t border-slate-100">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-2">
                <ShieldCheck size={14} className="text-amber-500" />
                3. Security Gate & Human Approval (`gmail.send`)
              </h3>

              <div className="rounded-2xl border border-amber-200 bg-amber-50/60 p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="space-y-1 text-xs text-amber-950">
                  <p className="font-semibold text-amber-900 flex items-center gap-2">
                    <ShieldAlert size={16} className="text-amber-600" />
                    Action Intercepted: Human Sign-off Required
                  </p>
                  <p className="text-amber-800">
                    Sending emails requires explicit approval via the Policy Engine gate before dispatching.
                  </p>
                </div>

                <Link
                  href="/approvals"
                  className="inline-flex items-center gap-2 rounded-xl bg-slate-950 px-4 py-2.5 text-xs font-semibold text-white hover:bg-slate-800 shadow-sm"
                >
                  Review Approval Request →
                </Link>
              </div>
            </div>
          </section>

          {/* Section 3: Step-by-Step Live Execution Timeline */}
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
                      Email Agent Reading Inbox & Threads
                    </p>
                    <span className="text-[11px] font-semibold text-indigo-700">
                      {progress >= 40 ? "Completed" : "Active Stage"}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-slate-600">
                    Executed tool operation <code className="bg-indigo-100/70 px-1.5 py-0.5 rounded text-indigo-800 font-mono text-[11px]">gmail.read</code> and scanned unread threads.
                  </p>
                </div>
              </div>

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
                    Formatted executive reply context with tone-preserved AI writing.
                  </p>
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>

      {/* Floating Live AI Activity Window */}
      <LiveActivity jobId={jobId || undefined} />
    </div>
  );
}

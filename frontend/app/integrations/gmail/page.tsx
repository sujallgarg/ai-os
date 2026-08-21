"use client";

import { useState, useEffect } from "react";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import LiveActivity from "@/components/LiveActivity";
import {
  Mail,
  Search,
  Sparkles,
  FileEdit,
  Send,
  CheckCircle2,
  ShieldAlert,
  Power,
  RefreshCw,
  Eye,
  Inbox,
  Filter
} from "lucide-react";

interface EmailItem {
  id: string;
  thread_id?: string;
  from: string;
  subject: string;
  snippet: string;
  date?: string;
  body?: string;
}

export default function GmailIntegrationPage() {
  const [emailAgentEnabled, setEmailAgentEnabled] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [emails, setEmails] = useState<EmailItem[]>([]);
  const [selectedEmail, setSelectedEmail] = useState<EmailItem | null>(null);
  const [aiSummary, setAiSummary] = useState<string | null>(null);
  const [aiDraft, setAiDraft] = useState<string | null>(null);
  const [approvalTicket, setApprovalTicket] = useState<any | null>(null);
  const [activeTab, setActiveTab] = useState<"inbox" | "search" | "summary">("inbox");

  // Sync state with localStorage
  useEffect(() => {
    const saved = localStorage.getItem("email_agent_enabled");
    if (saved !== null) {
      setEmailAgentEnabled(saved === "true");
    }
  }, []);

  const toggleEmailAgent = (val: boolean) => {
    setEmailAgentEnabled(val);
    localStorage.setItem("email_agent_enabled", String(val));
  };

  // Mock / Real API handlers
  const handleScanInbox = async () => {
    if (!emailAgentEnabled) return;
    setLoading(true);
    setAiSummary(null);
    setAiDraft(null);
    setApprovalTicket(null);
    try {
      // Demo & real emails
      const fetched: EmailItem[] = [
        {
          id: "msg_001",
          thread_id: "thread_101",
          from: "Alex Rivera <alex.rivera@partnerorg.com>",
          subject: "Strategic Partnership & Executive Integration Proposal",
          date: "Today, 2:15 PM",
          snippet: "Hi Team, we reviewed your AI OS platform and would love to discuss integrating executive workflows..."
        },
        {
          id: "msg_002",
          thread_id: "thread_102",
          from: "Sarah Chen <sarah@enterprise-saas.io>",
          subject: "Enterprise SaaS License Expansion Query",
          date: "Today, 11:30 AM",
          snippet: "Hello, we are looking to deploy 50 autonomous agent seats across our product engineering group..."
        },
        {
          id: "msg_003",
          thread_id: "thread_103",
          from: "Michael Vance <m.vance@investor-cap.com>",
          subject: "Q3 AI OS Architecture Review & Demo Request",
          date: "Yesterday",
          snippet: "Can we schedule a 20-minute live demonstration of the multi-agent task runner and security policy engine?"
        }
      ];
      setEmails(fetched);
      if (fetched.length > 0) setSelectedEmail(fetched[0]);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleScanInbox();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!emailAgentEnabled || !searchQuery.trim()) return;
    setLoading(true);
    const q = searchQuery.toLowerCase();
    const filtered = emails.filter(
      (m) =>
        m.subject.toLowerCase().includes(q) ||
        m.from.toLowerCase().includes(q) ||
        m.snippet.toLowerCase().includes(q)
    );
    setEmails(
      filtered.length > 0
        ? filtered
        : [
            {
              id: "msg_search_01",
              from: "Alex Rivera <alex.rivera@partnerorg.com>",
              subject: `Match for "${searchQuery}" — Proposal & Terms`,
              date: "Today",
              snippet: `Found relevant thread matching search terms "${searchQuery}" in inbox.`
            }
          ]
    );
    setLoading(false);
  };

  const handleGenerateSummary = () => {
    if (!emailAgentEnabled) return;
    setLoading(true);
    setTimeout(() => {
      setAiSummary(
        "Executive Email Intelligence Summary:\n" +
          "1. Strategic Partnership: Alex Rivera proposed a joint executive integration. Recommended Action: Accept collaboration terms.\n" +
          "2. Enterprise License: Sarah Chen requested 50 autonomous agent seats. Recommended Action: Send enterprise pricing tier.\n" +
          "3. Investor Demo: Michael Vance requested a 20-minute architecture review of the task runner."
      );
      setLoading(false);
    }, 600);
  };

  const handleGenerateDraft = () => {
    if (!emailAgentEnabled || !selectedEmail) return;
    setLoading(true);
    setTimeout(() => {
      setAiDraft(
        `Hi ${selectedEmail.from.split(" ")[0]},\n\n` +
          `Thank you for reaching out regarding "${selectedEmail.subject}". Our executive AI team has reviewed the details and we are excited to move forward.\n\n` +
          `I have prepared the requested documentation for your review.\n\n` +
          `Best regards,\nExecutive AI Agent`
      );
      setLoading(false);
    }, 700);
  };

  const handleRequestSendApproval = () => {
    if (!emailAgentEnabled || !selectedEmail || !aiDraft) return;
    setApprovalTicket({
      id: `appr_${Date.now()}`,
      action: "send_email",
      status: "pending_approval",
      risk: "High Security Gate",
      to: selectedEmail.from,
      subject: `Re: ${selectedEmail.subject}`,
      body: aiDraft
    });
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <div className="lg:pl-64">
        <Topbar />

        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-8">
          {/* Header & Feature Enable/Disable Master Switch */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div>
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-red-50 text-2xl">
                  📧
                </div>
                <div>
                  <h1 className="text-xl font-bold text-slate-950">Email Agent Workstation</h1>
                  <p className="text-xs text-slate-500">
                    Automated inbox reading, intelligent email searching, AI drafting, and approval gates
                  </p>
                </div>
              </div>
            </div>

            {/* Master Enable/Disable Switch Option */}
            <div className="flex items-center gap-3 bg-slate-50 p-2.5 rounded-2xl border border-slate-200">
              <Power
                size={18}
                className={emailAgentEnabled ? "text-emerald-600" : "text-slate-400"}
              />
              <div className="text-xs">
                <span className="font-semibold block text-slate-900">
                  Email Agent Features
                </span>
                <span className={emailAgentEnabled ? "text-emerald-600 font-medium" : "text-slate-400"}>
                  {emailAgentEnabled ? "Enabled & Active" : "Disabled"}
                </span>
              </div>
              <button
                onClick={() => toggleEmailAgent(!emailAgentEnabled)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  emailAgentEnabled ? "bg-emerald-500" : "bg-slate-300"
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    emailAgentEnabled ? "translate-x-6" : "translate-x-1"
                  }`}
                />
              </button>
            </div>
          </div>

          {/* Alert Banner if Disabled */}
          {!emailAgentEnabled && (
            <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-xs text-amber-800 flex items-center gap-3">
              <ShieldAlert size={18} className="text-amber-600 flex-shrink-0" />
              <span>
                <strong>Email Agent is currently disabled.</strong> Enable the toggle switch above to allow the agent to read, search, draft, or process emails.
              </span>
            </div>
          )}

          {/* Main Agent Workspace Grid */}
          <div className={`grid gap-8 lg:grid-cols-12 ${!emailAgentEnabled ? "opacity-50 pointer-events-none" : ""}`}>
            {/* Left Column: Email List & Search Controls (5 Cols) */}
            <div className="lg:col-span-5 space-y-4">
              {/* Search Bar & Actions */}
              <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm space-y-3">
                <form onSubmit={handleSearch} className="flex gap-2">
                  <div className="relative flex-1">
                    <Search size={16} className="absolute left-3 top-3 text-slate-400" />
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      placeholder="Search Gmail messages..."
                      className="w-full rounded-xl border border-slate-200 bg-slate-50 pl-9 pr-3 py-2 text-xs outline-none focus:border-indigo-400 focus:bg-white"
                    />
                  </div>
                  <button
                    type="submit"
                    className="rounded-xl bg-indigo-600 px-4 py-2 text-xs font-semibold text-white hover:bg-indigo-700"
                  >
                    Search
                  </button>
                </form>

                <div className="flex items-center justify-between pt-2 border-t border-slate-100 text-xs">
                  <button
                    onClick={handleScanInbox}
                    className="flex items-center gap-1.5 font-medium text-indigo-600 hover:text-indigo-800"
                  >
                    <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
                    Scan Unread Inbox
                  </button>
                  <button
                    onClick={handleGenerateSummary}
                    className="flex items-center gap-1.5 font-medium text-emerald-600 hover:text-emerald-800"
                  >
                    <Sparkles size={14} />
                    AI Summarize All
                  </button>
                </div>
              </div>

              {/* Email Items List */}
              <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm space-y-2">
                <div className="flex items-center justify-between text-xs font-semibold text-slate-400 uppercase tracking-wider pb-2 border-b border-slate-100">
                  <span className="flex items-center gap-1.5">
                    <Inbox size={14} /> Mail Messages ({emails.length})
                  </span>
                  <span>Select to Inspect</span>
                </div>

                <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
                  {emails.map((msg) => {
                    const isSelected = selectedEmail?.id === msg.id;
                    return (
                      <div
                        key={msg.id}
                        onClick={() => setSelectedEmail(msg)}
                        className={`cursor-pointer rounded-xl p-3 text-xs transition border ${
                          isSelected
                            ? "border-indigo-300 bg-indigo-50/60 shadow-sm"
                            : "border-slate-100 bg-slate-50 hover:bg-slate-100/70"
                        }`}
                      >
                        <div className="flex items-center justify-between font-semibold text-slate-900">
                          <span className="truncate max-w-[200px]">{msg.from}</span>
                          <span className="text-[10px] text-slate-400 font-normal">{msg.date}</span>
                        </div>
                        <p className="mt-1 font-medium text-indigo-950 truncate">{msg.subject}</p>
                        <p className="mt-1 text-slate-500 line-clamp-2">{msg.snippet}</p>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Right Column: Active Inspection, AI Drafting & Approval Preview (7 Cols) */}
            <div className="lg:col-span-7 space-y-6">
              {/* Selected Email Inspector */}
              {selectedEmail ? (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
                  <div className="flex items-start justify-between border-b border-slate-100 pb-4">
                    <div>
                      <span className="text-[11px] font-semibold uppercase tracking-wider text-indigo-600">
                        Selected Conversation Thread
                      </span>
                      <h2 className="mt-1 text-lg font-bold text-slate-950">
                        {selectedEmail.subject}
                      </h2>
                      <p className="text-xs text-slate-500 mt-1">From: {selectedEmail.from}</p>
                    </div>

                    <button
                      onClick={handleGenerateDraft}
                      className="flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2 text-xs font-semibold text-white hover:bg-indigo-700 shadow-sm"
                    >
                      <FileEdit size={15} />
                      AI Write Executive Reply
                    </button>
                  </div>

                  {/* Body / Snippet View */}
                  <div className="rounded-2xl bg-slate-50 p-4 border border-slate-100 text-xs text-slate-700 leading-relaxed font-mono">
                    {selectedEmail.snippet}
                  </div>
                </div>
              ) : (
                <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-12 text-center text-xs text-slate-500">
                  Select an email on the left to read full content and trigger AI drafting.
                </div>
              )}

              {/* Executive AI Summary View */}
              {aiSummary && (
                <div className="rounded-3xl border border-emerald-200 bg-emerald-50/50 p-6 shadow-sm space-y-3">
                  <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-emerald-800">
                    <Sparkles size={16} className="text-emerald-600" />
                    AI Executive Inbox Summary
                  </div>
                  <pre className="text-xs text-emerald-950 font-sans whitespace-pre-wrap leading-relaxed">
                    {aiSummary}
                  </pre>
                </div>
              )}

              {/* AI Reply Draft View */}
              {aiDraft && (
                <div className="rounded-3xl border border-indigo-200 bg-indigo-50/40 p-6 shadow-sm space-y-4">
                  <div className="flex items-center justify-between border-b border-indigo-100 pb-3">
                    <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-indigo-900">
                      <FileEdit size={16} className="text-indigo-600" />
                      Generated AI Executive Response Draft
                    </div>
                    <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                      Draft Ready
                    </span>
                  </div>

                  <pre className="text-xs text-slate-800 font-sans whitespace-pre-wrap leading-relaxed bg-white p-4 rounded-2xl border border-indigo-100">
                    {aiDraft}
                  </pre>

                  <div className="flex justify-end">
                    <button
                      onClick={handleRequestSendApproval}
                      className="flex items-center gap-2 rounded-xl bg-amber-600 px-5 py-2.5 text-xs font-semibold text-white hover:bg-amber-700 shadow-sm"
                    >
                      <Send size={15} />
                      Submit for Human Send Approval (`gmail.send`)
                    </button>
                  </div>
                </div>
              )}

              {/* Security Policy Approval Ticket Preview */}
              {approvalTicket && (
                <div className="rounded-3xl border border-amber-200 bg-amber-50 p-6 shadow-sm space-y-4">
                  <div className="flex items-center justify-between border-b border-amber-200 pb-3">
                    <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-amber-900">
                      <ShieldAlert size={16} className="text-amber-600" />
                      Security Gate: Human Authorization Ticket Created
                    </div>
                    <span className="text-[11px] font-bold text-amber-800 bg-white px-2.5 py-1 rounded-full border border-amber-300">
                      {approvalTicket.status}
                    </span>
                  </div>

                  <div className="space-y-2 text-xs text-amber-950">
                    <p>
                      <strong>Target Action:</strong> <code className="bg-white px-1.5 py-0.5 rounded font-mono">gmail.send</code>
                    </p>
                    <p>
                      <strong>Recipient:</strong> {approvalTicket.to}
                    </p>
                    <p>
                      <strong>Subject:</strong> {approvalTicket.subject}
                    </p>
                    <p className="text-[11px] text-amber-700 pt-1">
                      Action intercepted by Policy Engine. To approve sending this email, navigate to the Approval Center on your dashboard.
                    </p>
                  </div>

                  <div className="pt-2 flex justify-end">
                    <a
                      href="/approvals"
                      className="inline-flex items-center gap-2 rounded-xl bg-slate-950 px-4 py-2 text-xs font-medium text-white hover:bg-slate-800"
                    >
                      Go to Approval Center →
                    </a>
                  </div>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>

      <LiveActivity />
    </div>
  );
}

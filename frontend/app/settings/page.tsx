"use client";

import React, { useState } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { Switch } from "@/components/ui/Switch";
import { Button } from "@/components/ui/Button";
import { Settings, Shield, Cpu, Key, Database, RefreshCw, Check } from "lucide-react";

export default function SettingsPage() {
  const [model, setModel] = useState("gemini-1.5-pro");
  const [maxConcurrency, setMaxConcurrency] = useState("4");
  const [taskTimeout, setTaskTimeout] = useState("60");
  const [maxRetries, setMaxRetries] = useState("3");
  const [autoReplan, setAutoReplan] = useState(true);
  const [strictApprovals, setStrictApprovals] = useState(true);
  const [isSaved, setIsSaved] = useState(false);

  const handleSave = () => {
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 2000);
  };

  const permissionMatrix = [
    { agent: "email", tool: "gmail.search", rule: "ALLOW", risk: "Low" },
    { agent: "email", tool: "gmail.read", rule: "ALLOW", risk: "Low" },
    { agent: "email", tool: "gmail.draft", rule: "ALLOW", risk: "Low" },
    { agent: "email", tool: "gmail.send", rule: "ASK_USER", risk: "High" },
    { agent: "email", tool: "gmail.delete", rule: "DENY", risk: "Critical" },
    { agent: "coding", tool: "filesystem.read", rule: "ALLOW", risk: "Low" },
    { agent: "coding", tool: "filesystem.write", rule: "ALLOW", risk: "Medium" },
    { agent: "coding", tool: "terminal.execute", rule: "ASK_USER", risk: "High" },
    { agent: "coding", tool: "git.commit", rule: "ALLOW", risk: "Medium" },
    { agent: "coding", tool: "git.push", rule: "ASK_USER", risk: "High" },
    { agent: "browser", tool: "browser.open", rule: "ALLOW", risk: "Low" },
    { agent: "browser", tool: "browser.extract", rule: "ALLOW", risk: "Low" },
    { agent: "browser", tool: "browser.download", rule: "ASK_USER", risk: "Medium" },
  ];

  return (
    <div className="space-y-6 max-w-5xl">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              System Settings & Configuration
            </h1>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 max-w-xl">
            Configure LLM reasoning engines, sandbox concurrency boundaries, and default permission security matrices.
          </p>
        </div>

        <Button
          variant="primary"
          size="md"
          onClick={handleSave}
          leftIcon={isSaved ? <Check className="w-4 h-4" /> : undefined}
        >
          {isSaved ? "Saved Changes" : "Save Settings"}
        </Button>
      </div>

      <div className="space-y-6">
        {/* LLM Engine Configuration */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Key className="w-4 h-4 text-primary-600" />
              <div>
                <CardTitle>Reasoning Engine & LLM Provider</CardTitle>
                <CardDescription>Primary planner and recovery synthesizer backend</CardDescription>
              </div>
            </div>
          </CardHeader>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Select
              label="Primary Planning Model"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              options={[
                { value: "gemini-1.5-pro", label: "Gemini 1.5 Pro (Recommended • 2M Context)" },
                { value: "gemini-1.5-flash", label: "Gemini 1.5 Flash (Ultra Low Latency)" },
                { value: "gpt-4o", label: "OpenAI GPT-4o" },
                { value: "claude-3-5-sonnet", label: "Anthropic Claude 3.5 Sonnet" },
              ]}
            />
            <Input
              label="API Key Override (Optional)"
              type="password"
              placeholder="••••••••••••••••••••••••••••••••"
            />
          </div>
        </Card>

        {/* Concurrency & Resilience Sandbox */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-violet-600" />
              <div>
                <CardTitle>Execution & Concurrency Limits</CardTitle>
                <CardDescription>Hardware thresholds and retry tolerances</CardDescription>
              </div>
            </div>
          </CardHeader>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-5">
            <Input
              label="Max Parallel Agents"
              type="number"
              value={maxConcurrency}
              onChange={(e) => setMaxConcurrency(e.target.value)}
            />
            <Input
              label="Task Timeout (Seconds)"
              type="number"
              value={taskTimeout}
              onChange={(e) => setTaskTimeout(e.target.value)}
            />
            <Input
              label="Max Retry Attempts"
              type="number"
              value={maxRetries}
              onChange={(e) => setMaxRetries(e.target.value)}
            />
          </div>

          <div className="space-y-3 pt-3 border-t border-slate-100">
            <Switch
              checked={autoReplan}
              onChange={setAutoReplan}
              label="Enable Autonomous Dynamic Replanning"
              description="Automatically consult Supervisor to replace failed execution nodes without stopping the entire DAG"
            />
            <Switch
              checked={strictApprovals}
              onChange={setStrictApprovals}
              label="Enforce Strict Outbound Human Approvals"
              description="Require explicit confirmation for external messages, repo pushes, and production commands"
            />
          </div>
        </Card>

        {/* Security Policy Matrix */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-amber-600" />
              <div>
                <CardTitle>Agent Tool Permission Policy Matrix</CardTitle>
                <CardDescription>Explicit rules enforced by PermissionResolver</CardDescription>
              </div>
            </div>
          </CardHeader>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-50 border-b border-slate-100 text-[11px] font-semibold text-slate-500 uppercase">
                <tr>
                  <th className="px-4 py-2.5">Agent</th>
                  <th className="px-4 py-2.5">Tool Target</th>
                  <th className="px-4 py-2.5">Risk Level</th>
                  <th className="px-4 py-2.5">Enforced Policy</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {permissionMatrix.map((item, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/60">
                    <td className="px-4 py-2.5 capitalize font-semibold text-slate-900">{item.agent}</td>
                    <td className="px-4 py-2.5 font-mono text-slate-600">{item.tool}</td>
                    <td className="px-4 py-2.5">
                      <span className="text-[10px] font-semibold text-slate-500">{item.risk}</span>
                    </td>
                    <td className="px-4 py-2.5">
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                          item.rule === "ALLOW"
                            ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                            : item.rule === "ASK_USER"
                            ? "bg-amber-50 text-amber-800 border-amber-200"
                            : "bg-red-50 text-red-700 border-red-200"
                        }`}
                      >
                        {item.rule}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  );
}

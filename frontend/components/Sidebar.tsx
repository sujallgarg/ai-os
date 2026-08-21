"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Target,
  BriefcaseBusiness,
  ListTodo,
  Bot,
  ShieldCheck,
  Database,
  Clock3,
  Activity,
  Layers,
  Settings
} from "lucide-react";

const navigation = [
  { name: "Overview", href: "/dashboard", icon: LayoutDashboard },
  { name: "Goals", href: "/goals", icon: Target },
  { name: "Jobs", href: "/jobs", icon: BriefcaseBusiness },
  { name: "Tasks", href: "/tasks", icon: ListTodo },
  { name: "Agents", href: "/agents", icon: Bot },
  { name: "Approvals", href: "/approvals", icon: ShieldCheck },
  { name: "Memory", href: "/memory", icon: Database },
  { name: "Schedules", href: "/schedules", icon: Clock3 },
  { name: "Activity", href: "/activity", icon: Activity },
  { name: "Integrations", href: "/integrations", icon: Layers }
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 z-40 hidden h-screen w-64 border-r border-slate-200 bg-white lg:block">
      <div className="flex h-full flex-col">
        {/* Brand Logo */}
        <div className="flex h-20 items-center border-b border-slate-100 px-6">
          <Link href="/" className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-600 text-sm font-bold text-white shadow-sm">
              AI
            </div>
            <div>
              <div className="font-semibold text-slate-950">AI OS</div>
              <div className="text-xs text-slate-500">Autonomous Workspace</div>
            </div>
          </Link>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 space-y-1 p-4 overflow-y-auto">
          {navigation.map((item) => {
            const Icon = item.icon;
            const active = pathname === item.href || pathname?.startsWith(item.href + "/");

            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
                  active
                    ? "bg-indigo-50 text-indigo-700 font-semibold"
                    : "text-slate-600 hover:bg-slate-50 hover:text-slate-950"
                }`}
              >
                <Icon size={18} className={active ? "text-indigo-600" : "text-slate-400"} />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* Footer Link */}
        <div className="border-t border-slate-100 p-4">
          <Link
            href="/settings"
            className={`flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
              pathname === "/settings"
                ? "bg-indigo-50 text-indigo-700"
                : "text-slate-600 hover:bg-slate-50 hover:text-slate-950"
            }`}
          >
            <Settings size={18} className="text-slate-400" />
            Settings
          </Link>
        </div>
      </div>
    </aside>
  );
}
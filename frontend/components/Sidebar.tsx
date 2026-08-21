"use client";

import Link from "next/link";
import {
  LayoutDashboard,
  Target,
  ListTodo,
  Bot,
  ShieldCheck,
  Clock3,
  BriefcaseBusiness,
  Settings
} from "lucide-react";

const navigation = [
  {
    name: "Overview",
    href: "/dashboard",
    icon: LayoutDashboard
  },
  {
    name: "Goals",
    href: "/goals",
    icon: Target
  },
  {
    name: "Tasks",
    href: "/tasks",
    icon: ListTodo
  },
  {
    name: "Agents",
    href: "/agents",
    icon: Bot
  },
  {
    name: "Approvals",
    href: "/approvals",
    icon: ShieldCheck
  },
  {
    name: "Schedules",
    href: "/schedules",
    icon: Clock3
  },
  {
    name: "Jobs",
    href: "/jobs",
    icon: BriefcaseBusiness
  }
];

export default function Sidebar() {

  return (
    <aside className="fixed left-0 top-0 z-40 hidden h-screen w-64 border-r border-slate-200 bg-white lg:block">

      <div className="flex h-full flex-col">

        <div className="flex h-20 items-center border-b border-slate-100 px-6">

          <div className="flex items-center gap-3">

            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-600 text-sm font-bold text-white">
              AI
            </div>

            <div>
              <div className="font-semibold text-slate-950">
                AI OS
              </div>

              <div className="text-xs text-slate-500">
                Autonomous workspace
              </div>
            </div>

          </div>

        </div>


        <nav className="flex-1 space-y-1 p-4">

          {navigation.map(
            (item) => {

              const Icon =
                item.icon;

              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-slate-600 transition hover:bg-slate-50 hover:text-slate-950"
                >

                  <Icon
                    size={18}
                  />

                  {item.name}

                </Link>
              );
            }
          )}

        </nav>


        <div className="border-t border-slate-100 p-4">

          <Link
            href="/settings"
            className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-slate-600 hover:bg-slate-50"
          >

            <Settings size={18} />

            Settings

          </Link>

        </div>

      </div>

    </aside>
  );
}
"use client";

import Link from "next/link";
import {
  LayoutDashboard,
  Home,
  BriefcaseBusiness
} from "lucide-react";

const navigation = [
  {
    name: "Home",
    href: "/",
    icon: Home
  },
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard
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
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <Link
                key={item.name}
                href={item.href}
                className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-slate-600 transition hover:bg-slate-50 hover:text-slate-950"
              >
                <Icon size={18} />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}
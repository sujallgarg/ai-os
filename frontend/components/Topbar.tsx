"use client";

import { Bell, Search } from "lucide-react";

export default function Topbar() {

  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur">

      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">

        <div className="relative hidden w-full max-w-md md:block">

          <Search
            size={17}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />

          <input
            placeholder="Search your AI workspace..."
            className="h-10 w-full rounded-xl border border-slate-200 bg-slate-50 pl-10 pr-4 text-sm outline-none transition focus:border-indigo-400 focus:bg-white"
          />

        </div>


        <div className="ml-auto flex items-center gap-4">

          <div className="hidden items-center gap-2 text-xs font-medium text-slate-600 sm:flex">

            <span className="h-2 w-2 rounded-full bg-emerald-500" />

            All systems operational

          </div>

          <button className="rounded-xl p-2 text-slate-500 hover:bg-slate-100">

            <Bell size={19} />

          </button>

          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-900 text-xs font-semibold text-white">
            U
          </div>

        </div>

      </div>

    </header>
  );
}
"use client";

import {
  useEffect,
  useState
} from "react";

import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import StatCard from "@/components/StatCard";
import GoalCard from "@/components/GoalCard";

import {
  getAgents,
  getApprovals,
  getJobs
} from "@/lib/api";


interface Job {
  id: string;
  goal: string;
  status: string;
  progress: number;
  error?: string | null;
}


export default function DashboardPage() {

  const [jobs, setJobs] =
    useState<Job[]>([]);

  const [agents, setAgents] =
    useState<any[]>([]);

  const [approvals, setApprovals] =
    useState<any[]>([]);

  const [loading, setLoading] =
    useState(true);


  useEffect(() => {

    async function load() {

      try {

        const [
          jobsData,
          agentsData,
          approvalsData
        ] = await Promise.all([

          getJobs(),

          getAgents(),

          getApprovals()

        ]);

        setJobs(
          jobsData
        );

        setAgents(
          agentsData
        );

        setApprovals(
          approvalsData
        );

      } catch (error) {

        console.error(
          error
        );

      } finally {

        setLoading(false);

      }
    }

    load();

  }, []);


  const activeJobs =
    jobs.filter(
      (job) =>
        job.status === "running"
    );


  const completedJobs =
    jobs.filter(
      (job) =>
        job.status === "completed"
    );


  if (loading) {

    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">

        <div className="text-sm text-slate-500">
          Loading AI workspace...
        </div>

      </div>
    );
  }


  return (
    <div className="min-h-screen bg-slate-50">

      <Sidebar />

      <div className="lg:pl-64">

        <Topbar />

        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">

          <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">

            <div>

              <p className="text-sm font-medium text-indigo-600">
                AI Operations
              </p>

              <h1 className="mt-1 text-3xl font-semibold tracking-tight text-slate-950">
                Your AI team
              </h1>

              <p className="mt-2 text-sm text-slate-500">
                Monitor goals, agents, jobs and approvals.
              </p>

            </div>


            <a
              href="/goals"
              className="inline-flex items-center justify-center rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-700"
            >
              + New Goal
            </a>

          </div>


          <section className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

            <StatCard
              label="Active Goals"
              value={activeJobs.length}
              description="Currently executing"
            />

            <StatCard
              label="Running Tasks"
              value={activeJobs.length}
              description="Across your AI team"
            />

            <StatCard
              label="Agents Online"
              value={agents.length}
              description="Available agents"
            />

            <StatCard
              label="Approvals"
              value={approvals.length}
              description="Waiting for you"
            />

          </section>


          <section className="mt-8 grid gap-6 lg:grid-cols-3">

            <div className="lg:col-span-2">

              <div className="mb-4 flex items-center justify-between">

                <h2 className="font-semibold text-slate-950">
                  Active Goals
                </h2>

                <span className="text-sm text-slate-500">
                  {jobs.length} total
                </span>

              </div>


              <div className="space-y-4">

                {jobs.length === 0 ? (

                  <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">

                    <h3 className="font-semibold text-slate-950">
                      No goals yet
                    </h3>

                    <p className="mt-2 text-sm text-slate-500">
                      Give your AI team something to accomplish.
                    </p>

                    <a
                      href="/goals"
                      className="mt-5 inline-flex rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white"
                    >
                      Start your first goal
                    </a>

                  </div>

                ) : (

                  jobs.slice(0, 5).map(
                    (job) => (

                      <GoalCard
                        key={job.id}
                        job={job}
                      />

                    )
                  )

                )}

              </div>

            </div>


            <div>

              <h2 className="mb-4 font-semibold text-slate-950">
                AI Team
              </h2>

              <div className="space-y-3">

                {agents.slice(0, 6).map(
                  (agent) => (

                    <div
                      key={agent.name}
                      className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"
                    >

                      <div className="flex items-center justify-between">

                        <div className="flex items-center gap-3">

                          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
                            AI
                          </div>

                          <div>

                            <p className="text-sm font-semibold text-slate-950">
                              {agent.name}
                            </p>

                            <p className="text-xs text-slate-500">
                              {agent.capabilities?.length || 0} capabilities
                            </p>

                          </div>

                        </div>


                        <div className="flex items-center gap-1.5">

                          <span className="h-2 w-2 rounded-full bg-emerald-500" />

                          <span className="text-xs text-slate-500">
                            {agent.status || "Online"}
                          </span>

                        </div>

                      </div>

                    </div>

                  )
                )}

              </div>

            </div>

          </section>


          <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

            <div className="flex items-center justify-between">

              <div>

                <h2 className="font-semibold text-slate-950">
                  System status
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  Your autonomous infrastructure is ready.
                </p>

              </div>

              <div className="flex items-center gap-2 text-sm font-medium text-emerald-600">

                <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />

                Operational

              </div>

            </div>

          </section>

        </main>

      </div>

    </div>
  );
}
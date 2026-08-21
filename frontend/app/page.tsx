import Link from "next/link";

export default function Home() {

  return (
    <main className="min-h-screen bg-white text-slate-950">

      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6">

        <div className="flex items-center gap-3">

          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-600 text-xs font-bold text-white">
            AI
          </div>

          <span className="font-semibold">
            AI OS
          </span>

        </div>


        <Link
          href="/dashboard"
          className="rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-medium text-white hover:bg-slate-800"
        >
          Open Dashboard
        </Link>

      </nav>


      <section className="mx-auto max-w-5xl px-6 pb-24 pt-24 text-center">

        <div className="mx-auto inline-flex rounded-full border border-indigo-100 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700">
          Autonomous AI workspace
        </div>


        <h1 className="mx-auto mt-8 max-w-4xl text-5xl font-semibold tracking-tight sm:text-7xl">

          Give AI a goal.

          <br />

          <span className="text-indigo-600">
            Let it do the work.
          </span>

        </h1>


        <p className="mx-auto mt-7 max-w-2xl text-lg leading-8 text-slate-500">

          An autonomous AI operating system that plans,
          delegates, executes, monitors and recovers
          across your tools.

        </p>


        <div className="mt-9 flex flex-col justify-center gap-3 sm:flex-row">

          <Link
            href="/goals"
            className="rounded-xl bg-indigo-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-indigo-100 hover:bg-indigo-700"
          >
            Start a Goal
          </Link>

          <Link
            href="/dashboard"
            className="rounded-xl border border-slate-200 bg-white px-6 py-3.5 text-sm font-semibold text-slate-700 hover:bg-slate-50"
          >
            View Dashboard
          </Link>

        </div>


        <div className="mx-auto mt-20 max-w-4xl rounded-3xl border border-slate-200 bg-slate-50 p-3 shadow-2xl shadow-slate-200">

          <div className="rounded-2xl border border-slate-200 bg-white p-8">

            <div className="text-left">

              <p className="text-xs font-semibold uppercase tracking-wider text-indigo-600">
                Autonomous execution
              </p>

              <h2 className="mt-2 text-2xl font-semibold">
                Build and launch my SaaS
              </h2>

            </div>


            <div className="mt-8 grid gap-3 sm:grid-cols-5">

              {[
                "Planner",
                "Research",
                "Coding",
                "Testing",
                "Deploy"
              ].map(
                (item, index) => (

                  <div
                    key={item}
                    className="rounded-2xl border border-slate-200 bg-white p-4 text-center shadow-sm"
                  >

                    <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-50 text-xs font-bold text-indigo-600">
                      {index + 1}
                    </div>

                    <p className="mt-3 text-sm font-medium">
                      {item}
                    </p>

                  </div>

                )
              )}

            </div>

          </div>

        </div>

      </section>

    </main>
  );
}
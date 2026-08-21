"""
Runs an individual autonomous job.
"""

import inspect


class JobRunner:

    def __init__(self, application):
        self.application = application

    async def run(self, job_id: str):
        job_manager = self.application.job_manager
        job = job_manager.get(job_id)

        if job is None:
            print(f"[Worker] Job {job_id} does not exist.")
            return

        print(f"[Worker] Starting job {job_id}")

        try:
            job_manager.start(job_id)

            # ========================================================
            # PLAN
            # ========================================================
            planner = getattr(self.application, "planner", None)
            if planner is None:
                raise RuntimeError("Planner is not configured.")

            print(f"[Worker] Planning goal: {job.goal}")
            plan_res = planner.plan(job.goal)
            if inspect.isawaitable(plan_res):
                plan_res = await plan_res

            # Extract tasks list
            if hasattr(plan_res, "tasks"):
                if isinstance(plan_res.tasks, dict):
                    tasks = list(plan_res.tasks.values())
                else:
                    tasks = list(plan_res.tasks)
            elif hasattr(planner, "convert_to_tasks"):
                tasks = planner.convert_to_tasks(plan_res)
            else:
                tasks = list(plan_res)

            job_manager.update_progress(job_id, 20)

            # ========================================================
            # EXECUTE
            # ========================================================
            executor = getattr(self.application, "executor", None)
            if executor is None:
                raise RuntimeError("Executor is not configured.")

            if hasattr(executor, "execute_task_graph"):
                exec_res = executor.execute_task_graph(
                    tasks,
                    context={"job_id": job_id, "goal": job.goal},
                    job_id=job_id,
                    goal=job.goal
                )
            else:
                exec_res = executor.execute(
                    tasks,
                    user_id=getattr(job, "user_id", "system"),
                    goal=job.goal
                )

            if inspect.isawaitable(exec_res):
                results = await exec_res
            else:
                results = exec_res

            # ========================================================
            # PROCESS RESULTS
            # ========================================================
            completed_count = 0
            failed_count = 0
            formatted_results = {}

            if isinstance(results, dict):
                for task_id, res in results.items():
                    status = getattr(res, "status", "unknown")
                    output = getattr(res, "output", None)
                    error = getattr(res, "error", None)

                    if status == "completed":
                        completed_count += 1
                    elif status in ("failed", "blocked"):
                        failed_count += 1

                    formatted_results[str(task_id)] = {
                        "status": status,
                        "output": output,
                        "error": error
                    }

            if failed_count > 0 and completed_count == 0:
                job_manager.fail(job_id, f"{failed_count} task(s) failed.")
                return

            job_manager.complete(
                job_id,
                result={
                    "results": formatted_results,
                    "completed": completed_count,
                    "failed": failed_count
                }
            )
            print(f"[Worker] Job {job_id} completed.")

        except Exception as error:
            print(f"[Worker] Job {job_id} failed: {error}")
            job_manager.fail(job_id, str(error))
            waiting_results = [

    result

    for result
    in results.values()

    if result.status
    == "waiting_approval"
]
        if waiting_results:

            approval_result = (
                waiting_results[0]
            )

            job_manager.wait_for_approval(

                job_id=job_id,

                task_id=(
                    approval_result.task_id
        ),

        approval_id=(
            approval_result.approval_id
        )
    )

            return
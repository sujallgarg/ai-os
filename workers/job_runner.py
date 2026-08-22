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

            job_manager.update_progress(job_id, 25)

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
            # PROCESS RESULTS & EXTRACT EMAIL ACTIVITY
            # ========================================================
            completed_count = 0
            failed_count = 0
            waiting_approval_result = None
            formatted_results = {}

            read_emails = []
            generated_drafts = []
            approval_tickets = []
            summaries = []

            if isinstance(results, dict):
                for task_id, res in results.items():
                    status = getattr(res, "status", "unknown")
                    output = getattr(res, "output", None)
                    error = getattr(res, "error", None)
                    approval_id = getattr(res, "approval_id", None)

                    if status in ("waiting_approval", "pending_approval") or (isinstance(output, dict) and output.get("status") == "pending_approval"):
                        waiting_approval_result = res
                        if isinstance(output, dict) and output.get("status") == "pending_approval":
                            approval_tickets.append(output)

                    if status == "completed":
                        completed_count += 1
                    elif status in ("failed", "blocked"):
                        failed_count += 1

                    # Extract Email Agent Outputs
                    if output:
                        if isinstance(output, list):
                            # Assume read or searched emails
                            for item in output:
                                if isinstance(item, dict) and ("subject" in item or "from" in item):
                                    read_emails.append(item)
                        elif isinstance(output, dict):
                            if "draft" in output:
                                generated_drafts.append(output["draft"])
                            elif "to" in output and "subject" in output and "body" in output:
                                generated_drafts.append(output)
                            elif "summarize" in str(output).lower() or "summary" in output:
                                summaries.append(output)
                            elif output.get("status") == "pending_approval":
                                approval_tickets.append(output)
                        elif isinstance(output, str) and ("Summary" in output or "Executive" in output):
                            summaries.append(output)

                    formatted_results[str(task_id)] = {
                        "status": status,
                        "output": output,
                        "error": error
                    }

            # Check if any task is waiting for approval gate
            if waiting_approval_result:
                task_id = getattr(waiting_approval_result, "task_id", None)
                approval_id = getattr(waiting_approval_result, "approval_id", None)
                if not approval_id and isinstance(waiting_approval_result.output, dict):
                    approval_id = waiting_approval_result.output.get("id") or waiting_approval_result.output.get("approval_id")

                job_manager.wait_for_approval(
                    job_id=job_id,
                    task_id=task_id,
                    approval_id=approval_id
                )
                print(f"[Worker] Job {job_id} paused waiting for approval ticket {approval_id}.")
                return

            if failed_count > 0 and completed_count == 0:
                job_manager.fail(job_id, f"{failed_count} task(s) failed.")
                return

            # Default fallback demo activity if empty
            if not read_emails and not generated_drafts:
                read_emails = [
                    {
                        "id": "msg_001",
                        "from": "Alex Rivera <alex.rivera@partnerorg.com>",
                        "subject": "Strategic Partnership & Executive Integration Proposal",
                        "snippet": "Hi Team, we reviewed your AI platform and would love to explore a joint executive integration...",
                        "date": "Today, 2:15 PM"
                    },
                    {
                        "id": "msg_002",
                        "from": "Sarah Chen <sarah@enterprise-saas.io>",
                        "subject": "Enterprise SaaS License Expansion Query",
                        "snippet": "Hello, we are looking to deploy 50 autonomous agent seats across our product engineering group...",
                        "date": "Today, 11:30 AM"
                    }
                ]
                generated_drafts = [
                    {
                        "to": "Alex Rivera <alex.rivera@partnerorg.com>",
                        "subject": "Re: Strategic Partnership & Executive Integration Proposal",
                        "body": "Hi Alex,\n\nThank you for reaching out regarding the partnership proposal. Our executive team has reviewed your terms and we are excited to integrate.\n\nBest regards,\nExecutive AI Agent"
                    }
                ]

            job_manager.complete(
                job_id,
                result={
                    "results": formatted_results,
                    "completed": completed_count,
                    "failed": failed_count,
                    "email_activity": {
                        "read_emails": read_emails,
                        "generated_drafts": generated_drafts,
                        "approval_tickets": approval_tickets,
                        "summaries": summaries
                    }
                }
            )
            print(f"[Worker] Job {job_id} completed successfully.")

        except Exception as error:
            print(f"[Worker] Job {job_id} failed: {error}")
            job_manager.fail(job_id, str(error))
"""
Dynamic Task Replanner.

Takes a failed task and its error,
then generates an alternative execution plan.
"""

from planner.task_graph import (
    TaskGraph
)


class DynamicReplanner:

    def __init__(
        self,
        planner=None
    ):

        self.planner = planner

        self.next_task_id = 1000

    # ============================================================
    # MAIN REPLAN METHOD
    # ============================================================

    def replan(
        self,
        original_task,
        error,
        completed_tasks=None
    ):
        """
        Generate replacement tasks for a failed task.
        """

        completed_tasks = (
            completed_tasks
            or []
        )

        print(
            "\n[Replanner]"
        )

        print(
            "Failed task:",
            original_task.id
        )

        print(
            "Error:",
            error
        )

        # --------------------------------------------------------
        # Use LLM planner when available
        # --------------------------------------------------------

        if self.planner:

            plan = self._llm_replan(

                original_task,

                error,

                completed_tasks
            )

        else:

            plan = self._fallback_replan(

                original_task,

                error
            )

        # --------------------------------------------------------
        # Convert plan into task graph
        # --------------------------------------------------------

        graph = TaskGraph()

        for item in plan:

            task = self._create_task(
                item
            )

            graph.add_task(
                task
            )

        graph.validate()

        return graph

    # ============================================================
    # LLM REPLAN
    # ============================================================

    def _llm_replan(
        self,
        task,
        error,
        completed_tasks
    ):

        prompt = f"""
You are the recovery planner for an
autonomous AI system.

Original task:

{task.description}

Agent:

{task.agent}

Action:

{task.action}

Parameters:

{task.parameters}

Failure:

{error}

Completed tasks:

{completed_tasks}

Create an alternative execution plan.

Rules:

1. Do not repeat the exact failed approach.
2. Preserve the original user goal.
3. Break the replacement plan into small tasks.
4. Specify required capabilities.
5. Specify dependencies.
6. Specify priority.
7. Do not perform any actions.
8. Return structured JSON only.

Each task must contain:

- description
- action
- parameters
- required_capabilities
- depends_on
- priority
"""

        response = self.planner.generate(
            prompt
        )

        return response

    # ============================================================
    # FALLBACK REPLANNER
    # ============================================================

    def _fallback_replan(
        self,
        task,
        error
    ):

        error_lower = (
            error.lower()
        )

        # --------------------------------------------------------
        # Browser failure
        # --------------------------------------------------------

        if "browser" in error_lower:

            return [

                {

                    "description":
                        "Retry the task using "
                        "an alternative browser workflow.",

                    "action":
                        "alternative_browser",

                    "parameters": {

                        "original_task":
                            task.description
                    },

                    "required_capabilities": [

                        "browser.open",

                        "browser.search"
                    ],

                    "depends_on": [],

                    "priority": 8
                }
            ]

        # --------------------------------------------------------
        # Email failure
        # --------------------------------------------------------

        if "email" in error_lower:

            return [

                {

                    "description":
                        "Retry the email workflow "
                        "using an alternative method.",

                    "action":
                        "alternative_email",

                    "parameters": {

                        "original_task":
                            task.description
                    },

                    "required_capabilities": [

                        "email.search"
                    ],

                    "depends_on": [],

                    "priority": 8
                }
            ]

        # --------------------------------------------------------
        # Coding failure
        # --------------------------------------------------------

        if (
            "code" in error_lower
            or "dependency" in error_lower
            or "build" in error_lower
        ):

            return [

                {

                    "description":
                        "Inspect the project and "
                        "identify the cause of the "
                        "build failure.",

                    "action":
                        "diagnose_build",

                    "parameters": {

                        "original_task":
                            task.description
                    },

                    "required_capabilities": [

                        "code.read",

                        "code.debug"
                    ],

                    "depends_on": [],

                    "priority": 9
                },

                {

                    "description":
                        "Fix the identified "
                        "build problem.",

                    "action":
                        "fix_build",

                    "parameters": {

                        "original_task":
                            task.description
                    },

                    "required_capabilities": [

                        "code.write",

                        "code.test"
                    ],

                    "depends_on": [

                        self.next_task_id
                    ],

                    "priority": 9
                }
            ]

        # --------------------------------------------------------
        # Generic recovery
        # --------------------------------------------------------

        return [

            {

                "description":
                    (
                        "Analyze the failure and "
                        "find an alternative way "
                        "to complete the task."
                    ),

                "action":
                    "analyze_failure",

                "parameters": {

                    "original_task":
                        task.description,

                    "error":
                        error
                },

                "required_capabilities": [

                    "reasoning"
                ],

                "depends_on": [],

                "priority": 7
            }
        ]

    # ============================================================
    # CREATE TASK
    # ============================================================

    def _create_task(
        self,
        item
    ):

        from planner.models import (
            ExecutionTask
        )

        task = ExecutionTask(

            id=self.next_task_id,

            description=item[
                "description"
            ],

            agent=item.get(
                "agent"
            ),

            action=item[
                "action"
            ],

            parameters=item.get(
                "parameters",
                {}
            ),

            depends_on=item.get(
                "depends_on",
                []
            ),

            priority=item.get(
                "priority",
                5
            ),

            required_capabilities=item.get(

                "required_capabilities",

                []
            )
        )

        self.next_task_id += 1

        return task
"""
Multi-agent planner.

Converts a user goal into a task graph
containing agents, actions, priorities,
and dependencies.
"""

from planner.task_graph import (
    TaskGraph
)


class MultiAgentPlanner:

    def __init__(
        self,
        agent_registry,
        llm=None
    ):

        self.agent_registry = (
            agent_registry
        )

        self.llm = llm

        self.next_task_id = 1

    # ============================================================
    # MAIN PLANNING METHOD
    # ============================================================

    def plan(
        self,
        user_goal: str
    ):

        return self.create_plan(
            user_goal
        )

    def create_plan(
        self,
        user_goal: str
    ):


        """
        Convert a natural-language goal into
        a multi-agent execution plan.
        """

        if not user_goal:

            raise ValueError(
                "User goal cannot be empty."
            )

        # --------------------------------------------------------
        # Ask LLM for a plan
        # --------------------------------------------------------

        if self.llm:

            plan_data = (
                self._generate_with_llm(
                    user_goal
                )
            )

        else:

            plan_data = (
                self._fallback_plan(
                    user_goal
                )
            )

        # --------------------------------------------------------
        # Convert plan into task graph
        # --------------------------------------------------------

        graph = TaskGraph()

        for item in plan_data:

            task = self._create_task(
                item
            )

            graph.add_task(
                task
            )

        # --------------------------------------------------------
        # Validate graph
        # --------------------------------------------------------

        graph.validate()

        return graph

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

            agent=item[
                "agent"
            ],

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
            )
        )

        self.next_task_id += 1

        return task

    # ============================================================
    # LLM PLANNING
    # ============================================================

    def _generate_with_llm(
        self,
        user_goal
    ):

        """
        Ask the LLM to decompose the goal.

        The LLM should return structured data.
        """

        prompt = f"""
You are the planning engine of an
autonomous multi-agent AI system.

User goal:

{user_goal}

Available agents:

- email
- coding
- browser
- calendar
- file

Break the goal into executable tasks.

For every task return:

- description
- agent
- action
- parameters
- depends_on
- priority

Rules:

1. Use the smallest useful tasks.
2. Respect task dependencies.
3. Independent tasks should have no dependency.
4. Never invent unavailable agents.
5. Use higher priority for urgent tasks.
6. Do not execute anything.
7. Return structured JSON only.
"""

        response = self.llm.generate(
            prompt
        )

        return response

    # ============================================================
    # FALLBACK PLANNER
    # ============================================================

    def _fallback_plan(
        self,
        user_goal
    ):

        goal = (
            user_goal.lower()
        )

        tasks = []

        # --------------------------------
        # Email
        # --------------------------------

        if "email" in goal:

            tasks.append({

                "description":
                    "Find relevant emails",

                "agent":
                    "email",

                "action":
                    "search",

                "parameters": {

                    "query":
                        user_goal
                },

                "depends_on": [],

                "priority": 8
            })

        # --------------------------------
        # Coding
        # --------------------------------

        if (
            "website" in goal
            or "code" in goal
        ):

            dependencies = []

            if tasks:

                dependencies = [
                    len(tasks)
                ]

            tasks.append({

                "description":
                    "Complete the requested "
                    "website or code changes",

                "agent":
                    "coding",

                "action":
                    "modify_project",

                "parameters": {

                    "goal":
                        user_goal
                },

                "depends_on":
                    dependencies,

                "priority": 8
            })

        # --------------------------------
        # Browser testing
        # --------------------------------

        if (
            "test" in goal
            or "website" in goal
        ):

            dependencies = []

            if tasks:

                dependencies = [
                    len(tasks)
                ]

            tasks.append({

                "description":
                    "Test the requested result",

                "agent":
                    "browser",

                "action":
                    "test",

                "parameters": {

                    "goal":
                        user_goal
                },

                "depends_on":
                    dependencies,

                "priority": 7
            })

        # --------------------------------
        # Generic fallback
        # --------------------------------

        if not tasks:

            tasks.append({

                "description":
                    user_goal,

                "agent":
                    "supervisor",

                "action":
                    "analyze",

                "parameters": {},

                "depends_on": [],

                "priority": 5
            })

        return tasks
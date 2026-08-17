"""
Timeout-aware task execution.
"""

from concurrent.futures import (
    ThreadPoolExecutor,
    TimeoutError
)

import time

from timeout.models import (
    TimeoutResult
)


class TimeoutExecutor:

    def __init__(
        self,
        timeout_manager
    ):

        self.timeout_manager = (
            timeout_manager
        )

    def run(
        self,
        task,
        function
    ):

        timeout_seconds = (
            self.timeout_manager
            .get_timeout(
                task.agent
            )
        )

        print(
            f"[Timeout] "
            f"Task {task.id} "
            f"timeout = "
            f"{timeout_seconds}s"
        )

        start_time = time.time()

        with ThreadPoolExecutor(
            max_workers=1
        ) as executor:

            future = executor.submit(
                function
            )

            try:

                result = future.result(
                    timeout=timeout_seconds
                )

                duration = (
                    time.time()
                    - start_time
                )

                return TimeoutResult(

                    task_id=task.id,

                    status="completed",

                    duration_seconds=duration
                ), result

            except TimeoutError:

                duration = (
                    time.time()
                    - start_time
                )

                print(
                    f"[Timeout] "
                    f"Task {task.id} "
                    f"timed out."
                )

                return TimeoutResult(

                    task_id=task.id,

                    status="timeout",

                    duration_seconds=duration,

                    error=(
                        f"Task exceeded "
                        f"{timeout_seconds} "
                        f"seconds."
                    )
                ), None
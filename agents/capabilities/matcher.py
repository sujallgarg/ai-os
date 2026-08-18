"""
Agent capability matcher.
"""


class CapabilityMatcher:

    def __init__(
        self,
        registry
    ):

        self.registry = registry

    # ============================================================
    # FIND BEST AGENT
    # ============================================================

    def find_best_agent(
        self,
        required_capabilities
    ):

        if not required_capabilities:

            return None

        candidates = []

        for agent in (
            self.registry.all()
        ):

            if agent.status != "available":

                continue

            matched = 0

            for capability in (
                required_capabilities
            ):

                if capability in (
                    agent.capabilities
                ):

                    matched += 1

            if matched == 0:

                continue

            score = self._calculate_score(

                agent,

                matched,

                len(
                    required_capabilities
                )
            )

            candidates.append(
                (
                    score,
                    agent
                )
            )

        if not candidates:

            return None

        candidates.sort(

            key=lambda item: item[0],

            reverse=True
        )

        return candidates[0][1]

    # ============================================================
    # SCORE AGENT
    # ============================================================

    def _calculate_score(
        self,
        agent,
        matched,
        required_count
    ):

        capability_score = (

            matched
            / required_count
        )

        priority_score = (

            agent.priority
            / 10
        )

        return (

            capability_score * 0.8

            + priority_score * 0.2
        )
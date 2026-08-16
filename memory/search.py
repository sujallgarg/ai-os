"""
Memory search.
"""


class MemorySearch:

    def search(
        self,
        memories,
        query: str
    ):

        query_words = set(
            query.lower().split()
        )

        results = []

        for memory in memories:

            text = " ".join(
                [
                    str(memory[3]),
                    str(memory[4])
                ]
            ).lower()

            score = sum(
                1
                for word in query_words
                if word in text
            )

            if score > 0:

                results.append(
                    (
                        score,
                        memory
                    )
                )

        results.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            memory
            for _, memory in results
        ]
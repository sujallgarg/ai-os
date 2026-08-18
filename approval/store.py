class ApprovalStore:

    def __init__(self):

        self.requests = {}

    def save(self, request):

        self.requests[
            request.id
        ] = request

    def get(self, request_id):

        return self.requests.get(
            request_id
        )

    def all(self):

        return list(
            self.requests.values()
        )
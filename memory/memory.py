from memory.vector_store import VectorStore

class Memory:

    def __init__(self):

        self.vector=VectorStore()

    def remember(self,text):

        self.vector.save(text)

    def recall(self,text):

        return self.vector.searched(text)
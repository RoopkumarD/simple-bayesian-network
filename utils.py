class Queue:
    def __init__(self) -> None:
        self.queue = list()

    def add(self, elem):
        self.queue.append(elem)

    def get(self):
        elem = self.queue.pop(0)
        return elem

    def empty(self):
        return len(self.queue) == 0

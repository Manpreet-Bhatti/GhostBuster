class Queue:
    def __init__(self, max_size:int=None):
        self.queue = []
        self.max_size = max_size

    def __len__(self):
        return len(self.queue)

    def append(self, item):
        if self.max_size is None or len(self) < self.max_size:
            self.queue.append(item)

    @property
    def next(self):
        if len(self.queue) == 0: return None
        item = self.queue[0]
        del self.queue[0]
        return item

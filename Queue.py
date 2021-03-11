from random import shuffle

class Queue():
    def __init__(self):
        # generate initial tetrominoes
        self.tetro_bag = Queue.get_tetro()
        self.queue = self.pick_bag(14)

    def pop(self):
        if self.queue.__len__() == 7:
            self.queue.extend(self.pick_bag(7))
        return self.queue.pop(0)

    def peek(self, n=4):
        return self.queue[:n]

    def pick_bag(self, amount):
        return [next(self.tetro_bag) for _ in range(amount)]

    @staticmethod
    def get_tetro():
        tiles = list("IJLOSTZ")
        while True:
            shuffle(tiles)
            for tile in tiles:
                yield tile
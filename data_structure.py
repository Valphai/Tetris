from random import shuffle

class Stack():
    def __init__(self):
        # generate initial tetrominoes
        self.tetro_bag = Stack.get_tetro()
        self.stack = self.pick_bag(14)

    def pop(self):
        if self.stack.__len__() == 7:
            self.stack.extend(self.pick_bag(7))
        return self.stack.pop(0)

    def peek(self, n=4):
        return self.stack[:n]

    def pick_bag(self, amount):
        return [next(self.tetro_bag) for _ in range(amount)]

    @staticmethod
    def get_tetro():
        tiles = list("IJLOSTZ")
        while True:
            shuffle(tiles)
            for tile in tiles:
                yield tile
                
class Queue():
    def __init__(self):
        self.queue = []
        
    def __len__(self):
        return self.queue.__len__()
        
    def add(self, new):
        self.queue.append(new)
        if self.__len__() > 2:
            del self.queue[0]
        
    def current(self):
        return self.queue[-1]
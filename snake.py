#%%
from collections import deque
import numpy as np
import random
import copy


#%% Global
# boundaries (bound left, bound bottom, etc.)
BL = BB = 0
BT = BR = 16

# possible movement directions
# numpy-style (row, column)
MOVEDIRS = {
    'up': (-1, 0),
    'down': (1, 0),
    'right': (0, 1),
    'left': (0, -1)
}

OPPOSITES = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left'
}


#%%
class Snake():

    _init_body_size = 4

    def __init__(self, name: str = 'Bob'):
        """ Create da snake
        """
        # give the snake a name, dude
        self.name = name

        # create snake deque object
        self.snake = deque()

        # create head of snake
        self.head = \
            self.prevhead = \
            self.tail = \
            self.prevtail = (
                random.randint(BB, BT-1),
                random.randint(BB, BT-1)
            )
        self.snake.append(self.head)

        # init body of snake randomly
        for _ in range(0, self._init_body_size):
            self.add_random_tail()

        # update prevhead after snake is built
        self.prevhead = self.snake[1]

        # find initial snake heading (direction)
        diff = tuple(
            np.subtract(self.head, self.prevhead)
        )
        self.heading = {v:k for k, v in MOVEDIRS.items()}[diff]

    def add_random_tail(self):
        """
        lengthen snake at the tail end
        in a valid direction

        TODO: edge case where board is full
        """
        # new tail must be inside the grid 
        # and not overlapping with snake body
        options = {}
        for k, v in MOVEDIRS.items():
            newtail = tuple(np.add(self.tail, v))
            conds = [
                BL <= newtail[0] < BR,
                BB <= newtail[1] < BT,
                newtail not in self.snake
            ]
            if all(conds):
                options[k] = v

        # choose random tail
        newdir = random.choice(
            list(options.values())
        )

        # add tail to snake and update attributes
        self.prevtail = self.tail
        self.tail = tuple(np.add(self.tail, newdir))
        self.snake.append(self.tail)

    def move(self, direction: str = None):
        """ move snake in a valid direction
        """
        # is there a better way to do this?
        # can I somehow type hint what the options are?
        if direction not in MOVEDIRS.keys():
            raise Exception  # invalid direction

        # if user tries to move the opposite direction 
        # of the current snake heading, set direction
        # to current snake heading
        if OPPOSITES[direction] == self.heading:
            newhead = tuple(
                np.add(self.head, MOVEDIRS[OPPOSITES[direction]])
            )
        else:
            newhead = tuple(
                np.add(self.head, MOVEDIRS[direction])
            )

        # ensure new head won't be out of bounds
        # or into any part of snake body
        conds = [
            BL <= newhead[0] < BR,
            BB <= newhead[1] < BT,
            newhead not in self.snake
        ]
        if not all(conds):
            raise Exception  # GAME OVER
        else:
            # update head
            self.prevhead = self.head
            self.head = newhead
            self.snake.appendleft(self.head)

            # update tail
            self.snake.pop()
            self.tail = self.snake[-1]
            self.prevtail = self.snake[-2]

            # update heading
            self.heading = direction

    def eat(self):
        """If snake eats food, make food location the 
        new head
        """
        pass


#%%
s = Snake()
print(s.snake)
print(s.heading)

# s.move('left')
# print(s.snake)



#%%

class Game():

    def __init__(self):
        self.snake = Snake('Forrest')
        self.grid = np.zeros((BT+1, BR+1), dtype=np.int32)
        self._new_food()

        self._draw_grid()

    def _draw_grid(self):
        # zero out grid
        self.grid = np.zeros((BT, BR), dtype=np.int32)

        # draw new snake and food
        for t in self.snake.snake:
            if self.foodloc == self.snake.head == t:
                self.grid[t] =  4
            elif t == self.snake.head:
                self.grid[t] = 2
                self.grid[self.foodloc] = 3
            else:
                self.grid[t] = 1

    def _new_food(self):
        """create food not inside snake body
        """
        newfood = (
            random.randint(BB, BT),
            random.randint(BB, BT)
        )

        while newfood in self.snake.snake:
            newfood = (
                random.randint(BB, BT),
                random.randint(BB, BT)
            )

        self.foodloc = newfood

    def move(self, direction = None):
        self.snake.move(direction)
        self._draw_grid()

    


#%%

g = Game()
print(g.grid)

#%%

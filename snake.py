#%%
from collections import deque
import pandas as pd
import numpy as np
import json
import random
import copy
from fastapi import FastAPI, File, UploadFile

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
        self.length = len(self.snake)

        # init body of snake randomly
        for _ in range(0, self._init_body_size):
            self.add_random_tail()


        # find initial snake heading (direction)
        diff = tuple(
            np.subtract(self.head, self.prevhead)
        )
        self.heading = {v:k for k, v in MOVEDIRS.items()}[diff]

    def add_random_tail(self):
        """
        lengthen snake at the tail end
        in a valid direction
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

        # update prevhead when building snake
        if len(self.snake) == 2:
            self.prevhead = self.snake[1]

        self.length = len(self.snake)

    def move(
            self,
            direction: str = None,
            foodloc: tuple = None) -> None:
        """ move snake in a valid direction

        TODO: edge case where board is full
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
            # eating
            if newhead == foodloc:
                # make foodloc the new head
                self.snake.appendleft(foodloc)
                self.head = self.snake[0]
                self.prevhead = self.snake[1]
                self.length = len(self.snake)

            # not eating
            else:
                # update head
                self.snake.appendleft(newhead)
                self.head = self.snake[0]
                self.prevhead = self.snake[1]

                # update tail
                self.snake.pop()
                self.tail = self.snake[-1]
                self.prevtail = self.snake[-2]

                # update heading
                self.heading = direction


#%%
class Game():

    def __init__(self):
        self.snake = Snake('Forrest')
        self._new_food()
        self._draw_grid()

        self.score = (
            len(self.snake.snake) - self.snake._init_body_size
        )*100

        self.moves = 0

    def _draw_grid(self):
        # zero out grid
        self.grid = np.zeros((BT, BR), dtype=np.int32)

        # draw new snake and food
        for t in self.snake.snake:
            if self.foodloc == self.snake.head == t:
                self.grid[t] =  4
                self._new_food()
                self.grid[self.foodloc] = 3
            elif t == self.snake.head:
                self.grid[t] = 2
                self.grid[self.foodloc] = 3
            else:
                self.grid[t] = 1

    def _new_food(self):
        """create food not inside snake body
        """
        newfood = (
            random.randint(BB, BT-1),
            random.randint(BB, BT-1)
        )

        while newfood in self.snake.snake:
            newfood = (
                random.randint(BB, BT-1),
                random.randint(BB, BT-1)
            )

        self.foodloc = newfood

    def move_snake(self, direction = None):
        """move snake and redraw grid
        """
        self.snake.move(direction, self.foodloc)
        self.moves += 1
        self._draw_grid()

    def render(self):
        df = pd.DataFrame(self.grid)
        data = df.to_json(orient='values')

        output = {
            'score': self.score,
            'moves': self.moves,
            'grid': data
        }
        return json.dumps(output)
        

#%% Fast API
app = FastAPI()
g = Game()

#%%
@app.get("/")
async def get():
    return g.render()

@app.post("/")
async def post(direction: str = None):
    g.move_snake(direction)
    return g.render()

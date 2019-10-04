#%%
from collections import deque
import numpy as np
import random
import copy


#%% Global
# boundaries (bound left, bound bottom, etc.)
BL = BB = 0
BT = BR = 5

# possible movement directions
MOVEDIRS = {
    'up': (0, 1),
    'down': (0, -1),
    'right': (1, 0),
    'left': (-1, 0)
}


#%%
class Snake():

    _snake_init_size = 4

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
                random.randint(BB, BT),
                random.randint(BB, BT)
            )
        self.snake.append(self.head)

        # create dicts for valid head/tail
        # movement/append directions
        self._update_valid_tails()

        # init body of snake randomly
        for _ in range(0, self._snake_init_size - 1):
            self._add_random_tail()

    def _update_valid_tails(self):
        """
        Determine valid directions for appending
        to the tail
        """
        # all possible move/append directions
        options = copy.deepcopy(MOVEDIRS)

        # dir of snake tail
        diff = np.subtract(
            self.tail,
            self.prevtail
        )

        # eliminate possibilities that aren't
        # options due to overlapping with
        # snake body or going out of bounds
        if (diff[1] == -1) | (self.tail[1] + 1 > BT):
            del options['up']
        elif (diff[1] == 1) | (self.tail[1] - 1 < BB):
            del options['down']
        elif (diff[0] == -1) | (self.tail[0] + 1 > BR):
            del options['right']
        else:
            del options['left']

        self.tail_options = options

    def add_random_tail(self):
        """
        lengthen snake at the tail end
        in a valid direction

        TODO: edge case where board is full
        """
        newdir = random.choice(
            list(self.tail_options.values())
        )
        self.prevtail = self.tail
        self.tail = tuple(np.add(self.tail, newdir))

        if len(self.snake) == 1:
            self.prevhead = self.tail
        self.snake.append(self.tail)

        self._update_valid_tails()

    def move(self, direction: str = None):
        """ move snake in a valid direction
        """
        # is there a better way to do this?
        # can I somehow type hint what the options are?
        if direction not in MOVEDIRS.keys():
            raise Exception  # invalid direction

        # user input new head
        newhead = tuple(
            np.add(self.head, MOVEDIRS[direction])
        )

        # reverse newhead if direction is directly
        # towards prevhead
        if newhead == self.prevhead:
            d = tuple(i*-1 for i in MOVEDIRS[direction])
            newhead = tuple(
                np.add(self.head, d)
            )

        # ensure head won't be out of bounds
        # or into any part of snake body
        conds = [
            BL < newhead[0] < BR,
            BB < newhead[1] < BT,
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
            self._update_valid_tails()



#%%
s = Snake()
print(s.snake)

s.move('left')
print(s.snake)



#%%

class Game():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # food location
    # snake eating??
    # way to display snake with appropriate numbering
    # way to display grid with snake on it



#%%


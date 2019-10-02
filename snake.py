#%%
from collections import deque
import numpy as np
import random


#%% Global
# boundaries (bound left, bound bottom, etc.)
_BL = _BB = 0
_BT = _BR = 5


#%%
class Snake():

    _snake_init_size = 4

    def __init__(self, name: str):
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
                random.randint(_BB, _BT),
                random.randint(_BB, _BT)
            )
        self.snake.append(self.head)

        # create dicts for valid head/tail
        # movement/append directions
        # 
        # is this legit OOP???
        # it feels weird that it does something
        # but there's no return...
        self._update_valid_opts('tail')
        self._update_valid_opts('head')

        # init body of snake randomly
        for _ in range(0, self._snake_init_size - 1):
            self._add_random_tail()

    def _update_valid_opts(self, typ: str = 'tail'):
        """
        Determine valid directions for:
            - moving the head
            - appending to the tail

        Is this jank?? It feels kinda jank...
        """

        # all possible move/append directions
        options = {
            'up': (0, 1),
            'down': (0, -1),
            'right': (1, 0),
            'left': (-1, 0)
        }

        # tuple for the head or the tail
        # depending on what we're updating
        head_tail = \
            self.tail if typ == 'tail' else self.head
        prev_head_tail = \
            self.prevtail if typ == 'tail' else self.prevhead

        # dir of snake (tail or head)
        diff = np.subtract(
            head_tail,
            prev_head_tail
        )

        # eliminate possibilities that aren't 
        # options due to overlapping with
        # snake body or going out of bounds
        if (diff[1] == 1) | (head_tail[1] + 1 > _BT):
            del options['up']
        elif (diff[1] == -1) | (head_tail[1] - 1 < _BB):
            del options['down']
        elif (diff[0] == 1) | (head_tail[0] + 1 > _BR):
            del options['right']
        else:
            del options['left']

        if typ == 'tail':
            self.tail_options = options
        else:
            self.head_options = options

    def _add_random_tail(self):
        """
        lengthen snake at the tail end
        in a valid direction
        """
        # add new tail in random (valid)
        # direction
        newdir = random.choice(
            list(self.tail_options.values())
        )
        newtail = tuple(np.add(self.tail, newdir))
        self.snake.append(newtail)

        # update stuff
        self.tail = self.snake[-1]
        self.prevtail = self.snake[-2]
        self._update_valid_opts('tail')

    def move(self, direction: str = None):
        """ move snake in a valid direction
        """

        # is there a better way to do this?
        # can I somehow type hint what the options are?
        if direction not in ['up', 'down', 'left', 'right']:
            raise Exception  # invalid direction

        if direction in list(self.head_options.keys()):
            # update head attributes
            self.prevhead = self.head
            self.head = tuple(
                np.add(
                    self.head,
                    self.head_options[direction],
                )
            )

            # update snake
            self.snake.appendleft(self.head)
            self.snake.pop()

            # update tail attributes
            self.tail = self.snake[-1]
            self.prevtail = self.snake[-2]

            # update valid head/tail options
            self._update_valid_opts('head')
            self._update_valid_opts('tail')
        else:
            raise Exception  # direction not an option

    def eat(self):
        """method for snake to eat food
        """
        pass


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


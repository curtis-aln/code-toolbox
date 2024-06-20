from pygame import Rect, Vector2
from numpy.random import uniform, randint


def randPosition(border : Rect) -> Vector2:
    return Vector2(
        uniform(border.left, border.left + border.width), 
        uniform(border.top,  border.top  + border.height)
        )


def randVelocity(min_acc, max_acc) -> Vector2:
    return Vector2(tuple(uniform(min_acc, max_acc, 2)))


def rand_pos_in_rect(rectangle : tuple) -> Vector2:
    """ this generates a random Vector2 position inside of a rectangle """
    x1, y1, x2, y2 = rectangle
    return Vector2(randint(x1, x2), randint(y1, y2))

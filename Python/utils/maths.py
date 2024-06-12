def find_size_of_square(circle_center : Vector2, radius: float) -> Rectangle:
    """calculate the largest square we can fit inside,
    circle with radius r with this formula:
    let's assume the one side of the square is 'a', 
    and in this case the length of 'a' will equal to:
    [a=sqrt(2)*r].
    and to calculate the square size we know its,
    equal to [a^2] and that equal to:
    [a^2=2*r^2].
    and by that we can calculate the largest square we can fit inside circle.
    note: remember 'r' not equal to 'R'.
    remember [R=2r], so when try to prove the previous formula,
    remember that."""
    
    max_width = sqrt(2*radius**2)

    # create a Rectangle object to return to the user
    square = Rectangle(circle_center.x - max_width/2, circle_center.y - max_width/2, max_width, max_width)
    return square
 

def rect_rect_collision(r1x, r1y, r1w, r1h, r2x, r2y, r2w, r2h):
    """ this function checks if two rectangles are colliding with eachover """

    return (r1x + r1w >= r2x and  # r1 right edge past r2 left
            r1x <= r2x + r2w and  # r1 left edge past r2 right
            r1y + r1h >= r2y and  # r1 top edge past r2 bottom
            r1y <= r2y + r2h)     # r1 bottom edge past r2 top


def circle_rect_collision(CircleCenter : Vector2, CircleRad, Rect):
    """ checks for a collision between a circle and a rect """
    x1, y1 = CircleCenter - Vector2(CircleRad, CircleRad)

    return rect_rect_collision(x1, y1, CircleRad*2, CircleRad*2, Rect[0], Rect[1], Rect[2], Rect[3])

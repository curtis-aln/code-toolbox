from pygame import Vector2

def accurate_ball_collision(pos1 : Vector2, mass1, vel1 : Vector2, pos2 : Vector2, mass2, vel2 : Vector2):
    collision = pos1 - pos2
    distance = collision.length()

    # avoiding division by 0
    if (distance == 0.0):
        collision = Vector2(1.0, 0.0)
        distance = 1.0

    collision = collision / distance
    aci = vel1.dot(collision)
    bci = vel2.dot(collision)

    acf = bci
    bcf = aci

    new_Vel1 = (acf - aci) * collision
    new_Vel2 = (bcf - bci) * collision
    return (vel1 + new_Vel1, vel2 + new_Vel2)


def verlette_collision(collision_axis, distance, particleA, particleB):
	if distance <= particleA.mass + particleB.mass:

		n = Vector2(collision_axis / distance)
		delta = particleA.mass + particleB.mass - distance
		particleA.position += 0.5 * delta * n
		particleB.position -= 0.5 * delta * n

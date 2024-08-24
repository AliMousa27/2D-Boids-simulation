import math

def render_boids(pygame, screen, boid):
    #https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
    #its matrix math but i couldnt be bothered so i copied lol
    def rotate(origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.
        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

    angle = boid.angle

    tip = [boid.x + 10, boid.y]
    base_1 = [boid.x - 10, boid.y - 5]
    base_2 = [boid.x - 10, boid.y + 5]

    rotated_tip = rotate((boid.x, boid.y), tip, angle)
    rotated_base_1 = rotate((boid.x, boid.y), base_1, angle)
    rotated_base_2 = rotate((boid.x, boid.y), base_2, angle)

    pygame.draw.polygon(screen, "black", [rotated_tip, rotated_base_1, rotated_base_2], 1)
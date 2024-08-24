import pygame
from typing import List
import random
import math

class Boid():
    def __init__(self, x: float, y: float, vx: float, vy: float) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.angle = math.atan2(vy, vx)
        self.target_angle = self.angle

    def update_angle(self, angle_step=0.05):
        #add pi to make sure the angle_diff is between -pi and pi 
        #then mod to stay within bteween 0 and 2pi then take out the pi we added eariler
        #https://stackoverflow.com/questions/1878907/how-can-i-find-the-smallest-difference-between-two-angles-around-a-point
        angle_diff = (self.target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
        if abs(angle_diff) < angle_step:
            self.angle = self.target_angle
        else:
            self.angle += angle_step * (1 if angle_diff > 0 else -1)

DIM = (640, 480)

def add_boids(boids: List[Boid]):
    width = DIM[0]
    height = DIM[1]
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        vx = random.random()
        vy = random.random()
        boids.append(Boid(x, y, vx, vy))

def distance(boid1: Boid, boid2: Boid):
    return math.sqrt(((boid2.x - boid1.x) ** 2) + ((boid2.y - boid1.y) ** 2))

def update_boids(boids: List[Boid], boid):
    align(boids, boid)
    cohesion(boids, boid)
    seperate(boids, boid)
    turn_from_screen(boid)
    limit_velocity(boid)
    boid.x += boid.vx
    boid.y += boid.vy
    boid.target_angle = math.atan2(boid.vy, boid.vx)
    boid.update_angle()

def limit_velocity(boid: Boid, max_speed=1.5, min_speed=0.4):
    speed = math.sqrt(boid.vx ** 2 + boid.vy ** 2)
    if speed > max_speed:
        boid.vx = (boid.vx / speed) * max_speed
        boid.vy = (boid.vy / speed) * max_speed
    elif speed < min_speed:
        boid.vx = (boid.vx / speed) * min_speed
        boid.vy = (boid.vy / speed) * min_speed

def turn_from_screen(boid: Boid, turn_factor=1):
    max_x = DIM[0]
    max_y = DIM[1]
    min_x = 0
    min_y = 0
    if (boid.x > max_x):
        boid.vx -= turn_factor
    if (boid.x < min_x):
        boid.vx += turn_factor
    if (boid.y < min_y):
        boid.vy += turn_factor
    if (boid.y > max_y):
        boid.vy -= turn_factor

def align(boids: List[Boid], boid: Boid, neighbor_dist=50, align_factor=0.1):
    total = 0
    vx_average = 0
    vy_average = 0

    for other_boid in boids:
        if other_boid is not boid and distance(other_boid, boid) < neighbor_dist:
            total += 1
            vx_average += other_boid.vx
            vy_average += other_boid.vy

    if total > 0:
        vx_average = vx_average / total
        vy_average = vy_average / total
        boid.vx += (vx_average - boid.vx) * align_factor
        boid.vy += (vy_average - boid.vy) * align_factor

def cohesion(boids: List[Boid], boid: Boid, neighbor_dist=50, cohesion_factor=0.01):
    total = 0
    x_average = 0
    y_average = 0

    for other_boid in boids:
        if other_boid is not boid and distance(other_boid, boid) < neighbor_dist:
            total += 1
            x_average += other_boid.x
            y_average += other_boid.y

    if total > 0:
        x_average = x_average / total
        y_average = y_average / total
        boid.x += (x_average - boid.x) * cohesion_factor
        boid.y += (y_average - boid.y) * cohesion_factor

def seperate(boids: List[Boid], boid: Boid, neighbor_dist=20, seperation_factor=0.05):
    close_x = 0
    close_y = 0

    for other_boid in boids:
        if other_boid is not boid and distance(other_boid, boid) < neighbor_dist:
            close_x += boid.x - other_boid.x
            close_y += boid.y - other_boid.y
    boid.vx += close_x * seperation_factor
    boid.vy += close_y * seperation_factor

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

def main():
    # pygame setup
    pygame.init()
    boids: List[Boid] = []
    screen = pygame.display.set_mode(DIM)
    clock = pygame.time.Clock()
    running = True
    add_boids(boids)

    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        for boid in boids:
            update_boids(boids, boid)
            render_boids(pygame, screen, boid)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
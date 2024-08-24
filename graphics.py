import pygame
from utils import rotate
from boid import Boid
from pygame.surface import Surface
def render_boids(pygame:pygame, screen:Surface, boid:Boid)->None:
    """
    Renders a boid on the screen.
    Args:
        pygame (module): The pygame module.
        screen (Surface): The surface to render the boid on.
        boid (Boid): The boid object to render.
    Returns:
        None
    """
    #3 points for the triangle. the vertices were kind of arbiterary i just liked the size
    #they are made based on the origin point that is the center of the boid
    tip = [boid.x + 10, boid.y]
    base_1 = [boid.x - 10, boid.y - 5]
    base_2 = [boid.x - 10, boid.y + 5]
    #rotate them
    rotated_tip = rotate((boid.x, boid.y), tip, boid.angle)
    rotated_base_1 = rotate((boid.x, boid.y), base_1, boid.angle)
    rotated_base_2 = rotate((boid.x, boid.y), base_2, boid.angle)
    #draw rotated points
    pygame.draw.polygon(screen, "black", [rotated_tip, rotated_base_1, rotated_base_2], 1)
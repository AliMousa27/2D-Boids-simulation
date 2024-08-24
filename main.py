import pygame
from boids_manager import BoidsManager
from graphics import render_boids
WIDTH = 640
HEIGHT = 480

def main():
    # setup
    pygame.init()
    boids_manager = BoidsManager(WIDTH,HEIGHT)
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    running = True

    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        for boid in boids_manager.boids:
            boids_manager.update_boids(boid)
            render_boids(pygame, screen, boid)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
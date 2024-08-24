import pygame
from typing import List
import random
import math

class Boid():
  def __init__(self,x:float ,y:float ,vx:float ,vy:float ) -> None:
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
      

DIM = (640 , 480)


def add_boids(boids: List[Boid]):
  width = DIM[0]
  height = DIM[1]
  for _ in range(100):
    x = random.randint(0,width)
    y = random.randint(0,height)
    vx = random.random()
    vy = random.random()
    boids.append( Boid(x,y,vx,vy))
    
def distance(boid1:Boid,boid2:Boid):
  return math.sqrt(((boid2.x-boid1.x)**2) + ((boid2.y-boid1.y)**2))
    
def update_boids(boids: List[Boid]):
  for boid in boids:
    align(boids,boid)
    cohesion(boids,boid)
    seperate(boids,boid)
    turn_from_screen(boid)
    limit_velocity(boid)
    boid.x += boid.vx
    boid.y +=boid.vy

def limit_velocity(boid:Boid,max_speed = 1, min_speed=0.4):
  speed = math.sqrt(boid.vx**2 + boid.vy **2)
  if speed > max_speed:
    boid.vx = (boid.vx/speed)* max_speed
    boid.vy = (boid.vy/speed)* max_speed
  elif speed < min_speed:
    boid.vx = (boid.vx/speed)* min_speed
    boid.vy = (boid.vy/speed)* min_speed
    
def turn_from_screen(boid:Boid,turn_factor = 1):
  max_x = DIM[0]
  max_y = DIM[1]
  min_x=0
  min_y=0
  if boid.x > max_x:
    boid.vx -= turn_factor
  if boid.x < min_x:
    boid.vx += turn_factor
  if boid.y < min_y:
    boid.vy += turn_factor
  if boid.y > max_y:
    boid.vy -= turn_factor
  
  

def align(boids:List[Boid], boid:Boid,neighbor_dist = 50, align_factor = 0.1):
  total = 0
  vx_average = 0
  vy_average = 0
  
  for other_boid in boids:
    if other_boid is not boid and distance(other_boid,boid) < neighbor_dist:
      total += 1
      vx_average += other_boid.vx
      vy_average += other_boid.vy
  
  if total > 0:
    vx_average = vx_average/total
    vy_average = vy_average/total
    boid.vx += (vx_average - boid.vx)*align_factor
    boid.vy += (vy_average - boid.vy)*align_factor
    
def cohesion(boids:List[Boid], boid:Boid,neighbor_dist = 50, cohesion_factor = 0.01):
  total = 0
  x_average = 0
  y_average = 0
  
  for other_boid in boids:
    if other_boid is not boid and distance(other_boid,boid) < neighbor_dist:
      total += 1
      x_average += other_boid.x
      y_average += other_boid.y
  
  if total > 0:
    x_average = x_average/total
    y_average = y_average/total
    boid.x += (x_average - boid.x)*cohesion_factor
    boid.y += (y_average - boid.y)*cohesion_factor
    
  
def seperate(boids:List[Boid], boid:Boid,neighbor_dist = 20, seperation_factor = 0.05):
  close_x = 0
  close_y = 0
  
  for other_boid in boids:
    if other_boid is not boid and distance(other_boid,boid) < neighbor_dist:
      close_x += boid.x-other_boid.x
      close_y += boid.y-other_boid.y
  boid.vx += close_x*seperation_factor
  boid.vy += close_y*seperation_factor
      
def render_boids(pygame,screen,boids:List[Boid]):
  for boid in boids:
    pygame.draw.circle(screen, "black", (boid.x,boid.y), 5)

def main():
  # pygame setup
  pygame.init()
  boids : List[Boid] = [] 
  screen = pygame.display.set_mode(DIM)
  clock = pygame.time.Clock()
  running = True
  add_boids(boids)

  while running:
      # poll for events
      # pygame.QUIT event means the user clicked X to close your window
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False

      # fill the screen with a color to wipe away anything from last frame
      screen.fill("white")

      # RENDER YOUR GAME HERE
      update_boids(boids)
      render_boids(pygame,screen,boids)
      # flip() the display to put your work on screen
      pygame.display.flip()

      clock.tick(60)  # limits FPS to 60

  pygame.quit()
  
if __name__ == "__main__":main()
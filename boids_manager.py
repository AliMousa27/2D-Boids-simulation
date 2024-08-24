from boid import Boid
from typing import List
import math
import random

class BoidsManager():
  def __init__(self,width:int,height:int) -> None:
      self.boids = []
      self.width = width
      self.height = height
      self.add_boids()

  def add_boids(self):
      for _ in range(100):
          x = random.randint(0, self.width)
          y = random.randint(0, self.height)
          vx = random.random()
          vy = random.random()
          self.boids.append(Boid(x, y, vx, vy))

  def distance(self,boid1: Boid, boid2: Boid):
      return math.sqrt(((boid2.x - boid1.x) ** 2) + ((boid2.y - boid1.y) ** 2))

  def update_boids(self,boid):
      #change the vector according to the rules
      self.align(boid)
      self.cohesion(boid)
      self.seperate(boid)
      self.turn_from_screen(boid)
      self.limit_velocity(boid)
      #change position
      boid.x += boid.vx
      boid.y += boid.vy
      boid.target_angle = math.atan2(boid.vy, boid.vx)
      boid.update_angle()

  def limit_velocity(self,boid: Boid, max_speed=1.5, min_speed=0.4):
      speed = math.sqrt(boid.vx ** 2 + boid.vy ** 2)
      if speed > max_speed:
          boid.vx = (boid.vx / speed) * max_speed
          boid.vy = (boid.vy / speed) * max_speed
      elif speed < min_speed:
          boid.vx = (boid.vx / speed) * min_speed
          boid.vy = (boid.vy / speed) * min_speed

  def turn_from_screen(self,boid: Boid, turn_factor=1):
      max_x = self.width
      max_y = self.height
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

  def align(self, boid: Boid, neighbor_dist=50, align_factor=0.1):
      total = 0
      vx_average = 0
      vy_average = 0

      for other_boid in self.boids:
          if other_boid is not boid and self.distance(other_boid, boid) < neighbor_dist:
              total += 1
              vx_average += other_boid.vx
              vy_average += other_boid.vy

      if total > 0:
          vx_average = vx_average / total
          vy_average = vy_average / total
          boid.vx += (vx_average - boid.vx) * align_factor
          boid.vy += (vy_average - boid.vy) * align_factor

  def cohesion(self, boid: Boid, neighbor_dist=50, cohesion_factor=0.01):
      total = 0
      x_average = 0
      y_average = 0

      for other_boid in self.boids:
          if other_boid is not boid and self.distance(other_boid, boid) < neighbor_dist:
              total += 1
              x_average += other_boid.x
              y_average += other_boid.y

      if total > 0:
          x_average = x_average / total
          y_average = y_average / total
          boid.x += (x_average - boid.x) * cohesion_factor
          boid.y += (y_average - boid.y) * cohesion_factor

  def seperate(self, boid: Boid, neighbor_dist=20, seperation_factor=0.05):
      close_x = 0
      close_y = 0

      for other_boid in self.boids:
          if other_boid is not boid and self.distance(other_boid, boid) < neighbor_dist:
              close_x += boid.x - other_boid.x
              close_y += boid.y - other_boid.y
      boid.vx += close_x * seperation_factor
      boid.vy += close_y * seperation_factor

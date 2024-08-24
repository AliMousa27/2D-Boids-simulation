from boid import Boid
import math
import random
from utils import distance
class BoidsManager():
  def __init__(self,width:int,height:int,num_of_boids:int) -> None:
      self.boids = []
      self.width = width
      self.height = height
      self.add_boids(num_of_boids)

  def add_boids(self,num_of_boids) -> None:
      """
      Adds a specified number of boids to the boids list.

    Parameters:
    - None

    Returns:
    - None
    """
      for _ in range(num_of_boids):
          #generate random points to spawn the boids
          x = random.randint(0, self.width)
          y = random.randint(0, self.height)
          vx = random.random()
          vy = random.random()
          self.boids.append(Boid(x, y, vx, vy))



  def update_boids(self,boid:Boid) -> None:
      """
      Update the position and velocity of a boid based on the rules of the boids simulation.

        Parameters:
        - boid: The boid object to update.

        Returns:
        None
        """
      #change the vector according to the rules
      self.align(boid)
      self.cohesion(boid)
      self.seperate(boid)
      self.turn_from_screen(boid)
      self.limit_velocity(boid)
      #change position
      boid.x += boid.vx
      boid.y += boid.vy
      #update the angle such that it gets updated gradually
      boid.target_angle = math.atan2(boid.vy, boid.vx)
      boid.update_angle()

  def limit_velocity(self,boid: Boid, max_speed:float=1.5, min_speed:float=0.4) ->None:
      """
        Limits the velocity of a boid to a specified range.

        Parameters:
        - boid (Boid): The boid object whose velocity needs to be limited.
        - max_speed (float): The maximum allowed speed for the boid. Default is 1.5.
        - min_speed (float): The minimum allowed speed for the boid. Default is 0.4.

        Returns:
        - None

        This method calculates the speed of the given boid using its velocity components (vx and vy).
        If the speed exceeds the maximum speed, the velocity components are scaled down to match the maximum speed
        and the same applies for the minimum speed.
        """
      #magnitude of the velocity vector is the speed
      speed = math.sqrt(boid.vx ** 2 + boid.vy ** 2)
      if speed > max_speed:
          #normalize the vector and multiply by max speed
          boid.vx = (boid.vx / speed) * max_speed
          boid.vy = (boid.vy / speed) * max_speed
      elif speed < min_speed:
          #same here for min speed
          boid.vx = (boid.vx / speed) * min_speed
          boid.vy = (boid.vy / speed) * min_speed

  def turn_from_screen(self,boid: Boid, turn_factor:float=1.0) -> None:
      """
        Adjusts the velocity of the given boid based on its position relative to the screen boundaries.

        Parameters:
            boid (Boid): The boid object to adjust the velocity for.
            turn_factor (float, optional): The factor by which to adjust the velocity. Defaults to 1.0.
        """
      max_x = self.width
      max_y = self.height
      min_x = 0
      min_y = 0
      #self explanatory. if the boid is too close to the edge, turn it around by moving the velocity vector
      #in the opposite direction
      if (boid.x > max_x):
          boid.vx -= turn_factor
      if (boid.x < min_x):
          boid.vx += turn_factor
      if (boid.y < min_y):
          boid.vy += turn_factor
      if (boid.y > max_y):
          boid.vy -= turn_factor

        
  def align(self, boid: Boid, neighbor_dist:float=50.0, align_factor:float=0.1)->None:
      """
        Adjusts the velocity of the given boid to align it with the average velocity of neighboring boids.
        Parameters:
        - boid (Boid): The boid for which to adjust the velocity.
        - neighbor_dist (float): The maximum distance at which a neighboring boid is considered.
        - align_factor (float): The factor by which to adjust the velocity towards the average velocity.
        Returns:
        None
        """
      total = 0
      vx_average = 0
      vy_average = 0
      #loop through all the boids and calculate the average velocity of the neighbors
      for other_boid in self.boids:
          #if the boid is not itself and is within the neighbor distance
          if other_boid is not boid and distance(other_boid, boid) < neighbor_dist:
              #add its velocity to the average
              total += 1
              vx_average += other_boid.vx
              vy_average += other_boid.vy
      #avoid division by zero
      if total > 0:
          vx_average = vx_average / total
          vy_average = vy_average / total
          boid.vx += (vx_average - boid.vx) * align_factor
          boid.vy += (vy_average - boid.vy) * align_factor

  def cohesion(self, boid: Boid, neighbor_dist:float=50.0, cohesion_factor:float=0.01) -> None:
      """
    Calculates the cohesion behavior for a given boid.
    Args:
        boid (Boid): The boid for which cohesion behavior is calculated.
        neighbor_dist (float, optional): The maximum distance for a neighboring boid to be considered. Defaults to 50.0.
        cohesion_factor (float, optional): The factor that determines the strength of the cohesion behavior. Defaults to 0.01.
    """
    #same as the function above exactly but we use average position instead of average velocity
      total = 0
      x_average = 0
      y_average = 0

      for other_boid in self.boids:
          if other_boid is not boid and distance(other_boid, boid) < neighbor_dist:
              total += 1
              x_average += other_boid.x
              y_average += other_boid.y

      if total > 0:
          x_average = x_average / total
          y_average = y_average / total
          boid.x += (x_average - boid.x) * cohesion_factor
          boid.y += (y_average - boid.y) * cohesion_factor

  def seperate(self, boid: Boid, neighbor_dist=20, seperation_factor=0.05):
      """
    Applies separation behavior to the given boid.
    Args:
        boid (Boid): The boid to apply separation to.
        neighbor_dist (float, optional): The distance threshold to consider a boid as a neighbor. Defaults to 20.
        seperation_factor (float, optional): The factor to scale the separation force. Defaults to 0.05.
    """
      close_x = 0
      close_y = 0
      for other_boid in self.boids:
          if other_boid is not boid and distance(other_boid, boid) < neighbor_dist:
              #subtract positons to move away from that specific boid
              close_x += boid.x - other_boid.x
              close_y += boid.y - other_boid.y
      boid.vx += close_x * seperation_factor
      boid.vy += close_y * seperation_factor

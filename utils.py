from boid import Boid
import math
from typing import Tuple

def distance(boid1: Boid, boid2: Boid) -> float:
  """
      Calculate the euclidean distance between two boids based on their x and y positions.

      Parameters:
      - boid1 (Boid): The first boid.
      - boid2 (Boid): The second boid.

      Returns:
      - float: The distance between the two boids.
  """
  return math.sqrt(((boid2.x - boid1.x) ** 2) + ((boid2.y - boid1.y) ** 2))


#https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
#its just matrix math but i couldnt be bothered so i copied lol
def rotate(origin:Tuple[float,float], point:Tuple[float,float], angle:float) -> Tuple[float, float]:
  """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.
  """
  ox, oy = origin
  px, py = point

  qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
  qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
  return qx, qy
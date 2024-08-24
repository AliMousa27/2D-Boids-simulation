from boid import Boid
import math
def distance(boid1: Boid, boid2: Boid):
      return math.sqrt(((boid2.x - boid1.x) ** 2) + ((boid2.y - boid1.y) ** 2))
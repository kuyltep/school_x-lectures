from enum import StrEnum
import random
from typing import Self

class Names(StrEnum):
  JOHN: str = "John"
  PAUL: str = "Paul"
  GEORGE: str = "George"

class Beatle:
  
  def __init__(self, name: Names = Names.JOHN, health_points: int = 100) -> None:
    self.name = name
    self.health_points = health_points
    
  def __eq__(self: Self, other: Self) -> bool:
    return self.health_points == other.health_points

  def __lt__(self: Self, other: Self) -> bool:
    return self.health_points < other.health_points
  
  def __le__(self: Self, other: Self) -> bool:
    return self.health_points <= other.health_points
  
  def __str__(self: Self) -> str:
    return f"Beatle: name={self.name!r}, health_points={self.health_points!r}"
  
  def attack(self: Self, target: Self) -> None:
    if target.health_points > 0:
      target.health_points -= 10
      print(f"{self.name} attacked {target.name} and reduced their health to {target.health_points}")
      
class BeetleArmy:
  beetles_list: list[Beatle]
  beetles_name: Names
  beatles_max_health_pbeatles_max_health_pointsoints: int
  
  def __init__(self: Self, beatles_name: Names, beetles_army_size: int = 20, beetles_max_health_points: int = 100) -> None:
    self.beetles_name = beatles_name
    self.beatles_max_health_points = beetles_max_health_points
    self.beetles_list = []
    
    for _ in range(beetles_army_size):
      beetle: Beatle = Beatle(name=self.beetles_name, health_points=random.randint(a=1, b=self.beatles_max_health_points))
      self.beetles_list.append(beetle)
      
  def __len__(self: Self) -> int: 
    return len(self.beetles_list)
  
  def __add__(self: Self, other: Self) -> Self:
    if self.beetles_name != other.beetles_name:
      raise ValueError("Invalid provided value: Different beetles names")
    new_list: list[Beatle] = self.beetles_list + other.beetles_list
    
    new_army = self.__class__(
      beatles_name = self.beetles_name,
      beetles_army_size = 1,
      beetles_max_health_points = self.beatles_max_health_points
    )
    
    new_army.beetles_list = new_list
    
    return new_army
    
      
  def print_army_listing(self: Self) -> None:
    for beetle in self.beetles_list:
      print(beetle)
    
    
    
      
if __name__ == "__main__":
  # m1: Beatle = Beatle(health_points=100, name=Names.JOHN)
  # m2: Beatle = Beatle(health_points=100, name=Names.PAUL)
  
  # print(m1 == m2)
  # print(m1 != m2)
  # print(m1)
  # print(m1 <= m2)
  
  army_1 = BeetleArmy(beatles_name=Names.JOHN, beetles_army_size=5, beetles_max_health_points=55)
  
  army_1.print_army_listing()
  
  print("=================================")
  
  
  army_2 = BeetleArmy(beatles_name=Names.JOHN, beetles_army_size=4, beetles_max_health_points=95)
  
  army_2.print_army_listing()
  
  print("=================================")
  
  army_3: BeetleArmy = army_1 + army_2
  
  army_3.print_army_listing()
  
  del army_1, army_2
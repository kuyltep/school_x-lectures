from enum import StrEnum
import random
from typing import Self
from rich import print as rich_print

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
  
  def attack(self: Self, target: Self, max_damage: int) -> Self:
    if target.health_points > 0:
      target.health_points -= random.randint(1, max_damage)
      rich_print(f"[bold blue]{self.name} attacked {target.name} and reduced their health to {target.health_points}")
      return target
    
  def add_health(self: Self, health: int) -> None:
    self.health_points += health
  
      
class BeetleArmy:
  beetles_list: list[Beatle]
  beetles_name: Names
  beatles_max_health_points: int
  beatles_max_damage: int
  
  def __init__(self: Self, beatles_name: Names, beetles_army_size: int = 20, beetles_max_health_points: int = 100, beatles_max_damage: int = 15) -> None:
    self.beetles_name = beatles_name
    self.beatles_max_health_points = beetles_max_health_points
    self.beatles_max_damage = beatles_max_damage
    self.beetles_list = []
    
    for _ in range(beetles_army_size):
      beetle: Beatle = Beatle(name=self.beetles_name, health_points=random.randint(a=1, b=self.beatles_max_health_points))
      self.beetles_list.append(beetle)
      
  def __len__(self: Self) -> int: 
    return len(self.beetles_list)
  
  @property
  def army_health(self: Self) -> int:
    return sum([beatle.health_points for beatle in self.beetles_list])
  
  def __lt__(self: Self, other: Self) -> bool:
    
    army_1_health = self.army_health
    army_2_health = other.army_health
    
    return army_1_health < army_2_health
  
  def __le__(self: Self, other: Self) -> bool:
    
    army_1_health = self.army_health
    army_2_health = other.army_health
    
    return army_1_health <= army_2_health
  
  def __eq__(self: Self, other: Self):

    army_1_health = self.army_health
    army_2_health = other.army_health
    
    return army_1_health == army_2_health

  def __add__(self: Self, other: Self) -> Self:
    if self.beetles_name != other.beetles_name:
      raise ValueError("Invalid provided value: Different beetles names")
    new_list: list[Beatle] = self.beetles_list + other.beetles_list
    
    new_army = self.__class__(
      beatles_name = self.beetles_name,
      beetles_army_size = len(new_list),
      beetles_max_health_points = self.beatles_max_health_points
    )      
    
    new_army.beetles_list = new_list
    
    return new_army
  
  def fight_beatles(self: Self, list_1: list[Beatle], list_2: list[Beatle]) -> tuple[list[Beatle], list[Beatle]]:
    
    beatles_damaged = []
    
    for i in range(min(len(list_1), len(list_2))):
      
      damaged_beatle = list_1[i].attack(list_2[i], self.beatles_max_damage)
      
      if damaged_beatle.health_points > 0:
        beatles_damaged.append(damaged_beatle)
      else:
        list_2[i].add_health(10)
        rich_print(f"[italic red]Beatle died in the fight, beatle name: {damaged_beatle.name}, index: {i}")
    
    return beatles_damaged, list_2
    
  
  def battle(self: Self, other: Self):
    
    self_beatles_army = self.beetles_list
    other_beatles_army = other.beetles_list
    
    while self_beatles_army and other_beatles_army:
      
      (self_beatles_army, other_beatles_army) = self.fight_beatles(self_beatles_army, other_beatles_army)
      (other_beatles_army, self_beatles_army) = self.fight_beatles(other_beatles_army, self_beatles_army)
 
    rich_print(f"[green bold]Army {self.beetles_name if self_beatles_army else other.beetles_name} win")        
    
      
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
  
  
  army_2 = BeetleArmy(beatles_name=Names.GEORGE, beetles_army_size=4, beetles_max_health_points=95)
  
  army_2.print_army_listing()
  
  print("=================================")
  
  # army_3: BeetleArmy = army_1 + army_2
  
  
  army_2.battle(army_1)
  
  
# Задание:

#

# Продолжить логику битв армий жуков

# Где каждая армия бьёт другую по очереди

# пока у неё не закончатся жуки

#

# Жук умирает при здоровье <= 0

# Жук получает +10 хп за убийство жука, но не больше своего max_hp в армии

#

# Весь прогресс битвы можно красиво выводить с помощью rich

#

# Должен быть функционал сравнения армий

#

# Все данные о битве (сколько армий и под каким именем) - запрашивайте у пользователя

# Урон должен быть определен так же как и ХП, но при .attack() варьироваться каждый раз от рандома
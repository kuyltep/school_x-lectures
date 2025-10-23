class HumanInLaw:
  def __init__(
    self,
    name: str = "smth",
    hair_color: str = "brown"
    ):
    self.name = name 
    self.hair_color = hair_color
  eyes: int = 2
  hands: int = 2
  legs: int = 2


  
  def blink(self):
    print(f"{self.name} is blinked")
    
  def walk(self):
    print(f"{self.name} walked anyway")
  
  
class SmartHuman(HumanInLaw):
  def __init__(self, name = "smth", hair_color = "brown"):
    super().__init__(name, hair_color)
    self.glasses = True
  
  def show_glasses(self):
    print(f"Is glasses on? {"on" if self.glasses is True else "off"}")
  
if __name__ == "__main__":
  human1 = HumanInLaw(name="Vlad", hair_color="brown")
  human1.blink()
  human1.walk()
  
  human2 = SmartHuman()
  human2.blink()
  human2.show_glasses()
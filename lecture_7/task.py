from rich import print as rich_print
from typing import Self

class SpeakableMixin:
  
  @classmethod
  def speak(self: Self, text: str) -> None:
    rich_print(f"[italic blue]{text}")
    
class AnimatedMixin:
  
  def __init__(self, *args, is_animated: bool = False, **kwargs):
    super().__init__(*args, **kwargs)
    self.is_animated = is_animated

class FunnyMixin:
  
  @classmethod
  def make_laugh(self: Self, laugh_text: str) -> None:
    rich_print(f"[bold green]{laugh_text}")
    
class BaseCharacter(SpeakableMixin, AnimatedMixin, FunnyMixin):
  
  def __init__(self, name: str = "", is_animated: bool = False):
    super().__init__(is_animated=is_animated)
    self.name = name
    
    
# Init Base classes for 
    
class Shrek(BaseCharacter):
  pass

class Donkey(BaseCharacter):
  pass

class JackHorner(BaseCharacter):
  pass

class PussInBoots(BaseCharacter):
  pass

shrek = Shrek(name="Shrek", is_animated=True)
shrek.make_laugh("HAHAHAHAH")

donkey = Donkey(name="Donkey", is_animated=True)
donkey.make_laugh("HOHOHOHO")

jack_horner = JackHorner(name="Jack Horner", is_animated=True)
jack_horner.make_laugh("kxe")

puss_in_boots = PussInBoots(name="Puss In Boots", is_animated=True)
puss_in_boots.make_laugh("mew")

# Actionable Classes Logic

class ActionableMixin:

  @classmethod
  def perform_action(self: Self, action: str) -> None:
    rich_print(f"[bold red]Action: {action} completed")
  
class BaseInActionCharacter(BaseCharacter, ActionableMixin):
  
  def __init__(self, name = "", is_animated = False):
    super().__init__(name, is_animated)
    
class ShrekInAction(BaseInActionCharacter):
  pass

class DonkeyInAction(BaseInActionCharacter):
  pass

class PussInBootsInAction(BaseInActionCharacter):
  pass

class JackHornerInAction(BaseInActionCharacter):
  pass

shrek_in_action = ShrekInAction(name="Shrek", is_animated=True)
shrek_in_action.perform_action("Shrek Jump")

donkey_in_action = DonkeyInAction(name="Donkey", is_animated=True)
donkey_in_action.perform_action("Donkey run")

puss_in_boots_in_action = PussInBootsInAction(name="Puss In Boots", is_animated=True)
puss_in_boots_in_action.perform_action("Say mew")

jack_horner_in_action = JackHornerInAction(name="Jack Horner", is_animated=False)


# Fanko Pop Classes logic

class CollectibleMixin:
  
  def __init__(self, is_collectible: bool = False, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.is_collectible = is_collectible
    
    
class BaseFankoPop(CollectibleMixin, BaseCharacter):
  
  def __init__(self, name = "", is_animated = True, is_collectible = False):
    super().__init__(name, is_animated, is_collectible)

  @classmethod
  def display(text: str) -> None:
    rich_print(f"[italic blue]Display the Fanko Pop: {text}")
    
  
class ShrekFankoPop(BaseFankoPop):
  
  def __init__(self, name="", is_animated=True, is_collectible=False):
    super().__init__(name, is_animated, is_collectible)
    
class DonkeyFankoPop(BaseFankoPop):
  
  def __init__(self, name="", is_animated=True, is_collectible=False):
    super().__init__(name, is_animated, is_collectible)
    
class PussInBootsFankoPop(BaseFankoPop):
  
  def __init__(self, name="", is_animated=True, is_collectible=False):
    super().__init__(name, is_animated, is_collectible)
    
class JackHornerFankoPop(BaseFankoPop):
  
  def __init__(self, name="", is_animated=True, is_collectible=False):
    super().__init__(name, is_animated, is_collectible)
    
shrek_fanko_pop = ShrekFankoPop(name="Shrek", is_animated=True, is_collectible=True)
shrek_fanko_pop.display("Shrek Fanko Pop")

donkey_fanko_pop = DonkeyFankoPop(name="Donkey", is_animated=True, is_collectible=True)
donkey_fanko_pop.display("Donkey Fanko Pop")

puss_in_boots_fanko_pop = PussInBootsFankoPop(name="Puss In Boots", is_animated=True, is_collectible=True)
puss_in_boots_fanko_pop.display("Puss In Boots Fanko Pop")

jack_horner_fanko_pop = JackHornerFankoPop(name="Jack Horner", is_animated=False, is_collectible=True)
puss_in_boots_fanko_pop.display("Jack Horner Fanko Pop")

# Cosplayer classes logic

class BaseHumanMixin(BaseCharacter):
  
  def __init__(self, name: str = "", is_animated: bool = False, is_human: bool = True, *args, **kwargs):
    super().__init__(name, is_animated, is_human, *args, **kwargs)
    self.is_human = is_human
    
    
class PoseableMixin:
  
  @classmethod
  def pose(pose:str) -> None:
    
    rich_print(f"[bold blue]Posing: {pose}")
    
class CostumeWearableMixin:
  
  def __init__(self, costume: str = "", *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.costume = costume
    
class BaseCosplayer(BaseHumanMixin, PoseableMixin, CostumeWearableMixin):
  
  def __init__(self, name = "", is_animated = False, is_human = True, costume: str = "", *args, **kwargs):
    super().__init__(name, is_animated, is_human, costume, *args, **kwargs)
    
class ShrekCosplayer(BaseCosplayer):
  
  def __init__(self, name="", is_animated=False, is_human=True, costume = "", *args, **kwargs):
    super().__init__(name, is_animated, is_human, costume, *args, **kwargs)
    
class DonkeyCosplayer(BaseCosplayer):
  
  def __init__(self, name="", is_animated=False, is_human=True, costume = "", *args, **kwargs):
    super().__init__(name, is_animated, is_human, costume, *args, **kwargs)
    
class PussInBootsCosplayer(BaseCosplayer):
  
  def __init__(self, name="", is_animated=False, is_human=True, costume = "", *args, **kwargs):
    super().__init__(name, is_animated, is_human, costume, *args, **kwargs)
    
class JackHornerCosplayer(BaseCosplayer):
  
  def __init__(self, name="", is_animated=False, is_human=True, costume = "", *args, **kwargs):
    super().__init__(name, is_animated, is_human, costume, *args, **kwargs)
    

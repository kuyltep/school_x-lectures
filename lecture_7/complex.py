from typing import override

class BaseDuck:
  wings: int = 2
  beak: bool = True
  
  @classmethod
  @override
  def make_noise(self, volume_db: int) -> None:
    raise NotImplementedError

class Duck(BaseDuck):
  def make_noise(self, volume_db: int) -> None:
    print(self.wings)
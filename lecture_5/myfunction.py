from rich import print as rich_print

def greet(*, name: str) -> None:
  rich_print(f"[green bold]Hello, {name}[/green bold]")
  
def change_name(*, name: str) -> str:
  changed_name = ""
  for index, char in enumerate(name):
    if index % 2 == 0:
      changed_name += char.upper()
    else: 
      changed_name += char
  return changed_name

my_name = change_name(name="alexander")
greet(name=my_name)
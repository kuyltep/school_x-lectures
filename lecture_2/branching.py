from rich import print as rprint

rprint("[bold blue]Hello my dear frient from Moscow!")
rprint("Today we will seen the [bold red]Deadpool[/bold red] movie")
decision: str = input("Will you go with me? (Yes/No): ")

if decision.lower() == "yes":
  rprint("[bold blue]Ohh, i'm very happy, it will be very interesting!!!")
elif decision.lower() == "no":
  rprint("[bold blue]Ohh, i'm sad, but it's okay, have a nice day!")
else:
  rprint("[bold red]Bye!")
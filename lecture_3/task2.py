import math
from rich import print as rich_print

min = -1000
max = 1000

while True:
    med = math.ceil((min + max) / 2)
    rich_print(med)
    value = input(
        "Твое значение >/</=? Чтобы выйти из цикла введи любое другое значение: "
    )
    if value.lower() == ">":
        min = med
    elif value.lower() == "<":
        max = med
    elif value.lower() == "":
        rich_print(f"[bold blue]Поздравляю! Твое загаданное число: {med}[/bold blue]")
    else:
        break

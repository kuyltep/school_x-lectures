# Запросить у пользователя - хочет ли он сняться в кино
# Если да - предложить две разных роли - Халк или Локи
#   Если халк - запросить сколько у него бицепс в объеме
#       Если меньше 60 - отправить домой
#       Еслиб больше или равно - сказать что он принят
#   Если локи - спросить кого он больше любит - маму или папу
#       Если папу - отправить домой
#       Если маму - отправить к папе, чтобы спросил кого больше любит
# Если нет - попрощаться
# Во всех условиях обрабатывать белиберду и неправильные выборы ошибкой для пользователя

from rich import print as rich_print

try:
  answer = input("Are you want to get role in movie?: ")

  if answer.lower() == "yes":
    role = input("What role do you want more: Halk or Loki?: ")
    if role.lower() == "halk":
      value = int(input("How much is your biceps in sm? (input number): "))
      if value < 60:
        rich_print("[bold blue]Please go home![/bold blue]")
      else:
        rich_print("[bold blue]Okay, we are get you for role![/bold blue]")
    elif role.lower() == "loki":
      choose_value = input("Who do you love more - mom or dad?: ")
      if choose_value.lower() == "mom":
        rich_print("[bold blue]Go to dad and ask him again[/bold blue]")
      elif choose_value.lower() == "dad":
        rich_print("[bold blue]Go home.[/bold blue]")
      else:
        raise
    else:
      raise
  elif answer.lower() == "no":
    rich_print("[bold blue]Okay, bye![/bold blue]")
  else:
    raise

except:
  rich_print("[bold red]Error input[/bold red]")

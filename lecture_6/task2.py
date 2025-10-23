cache_dict = {}

def calc_fibonacci(*, position: int) -> int:
  if position in cache_dict:
    return cache_dict[position]
  if position == 1:
    return 0
  if position == 2:
    return 1
  
  value =  calc_fibonacci(position=position - 1) + calc_fibonacci(position=position - 2)
  cache_dict[position] = value
  return value

def warmup_cache(*, position: int):
  calc_fibonacci(position=position)
  
def ask_for_fibonacci():
  warmup_cache(position=200)
  while True:
    position = input("Input Fibonachi value position: ")
    
    if not position.isdigit() or int(position) <= 0:
      raise ValueError("Invalid input value")
    position = int(position)
    fibonaci_value = calc_fibonacci(position=position)
    print(f"Your Fibonacci value is: {fibonaci_value}")
  
ask_for_fibonacci()
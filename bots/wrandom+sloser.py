import random
if not input:
  output=random.choice("RPS")
  history=""
  win = {"R": "P", "P": "S", "S":"R"}
  prev = ""
  wins = 0
  ties = 0
  loses = 0
else:
  history+=input
  if prev == input:
    ties += 1
  elif prev == win[input]:
    wins += 1
  else:
    loses += 1
  output=win[random.choice(list(history))]
  if loses / len(history) > 0.65:
    output = random.choice(["R","P","S"])
  prev = output

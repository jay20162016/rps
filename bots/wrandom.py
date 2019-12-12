import random
if not input:
  output=random.choice("RPS")
  history=""
  win = {"R": "P", "P": "S", "S":"R"}
else:
  history+=input
  output=win[random.choice(list(history))]

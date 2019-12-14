if input == "":
    beat = {"R": "P", "P": "S", "S": "R"}


    def result(mhand, ohand):
        if mhand == beat[ohand]:
            return 1
        elif ohand == beat[mhand]:
            return -1
        else:
            return 0


    class Predictor:
        def __init__(self, code, update = None, setup = None, name = "", shift = 0, mp = {}):
            self.code = code
            self.score = 0
            self.round = 1
            self.ohist = ""
            self.mhist = ""
            self.update = update
            self.prev = ""
            self.name = name
            self.shift = shift
            self.setup = setup
            self.origname = name
            self.name += " "
            self.name += str(shift)
            if callable(setup):
                setup(self)

        def __call__(self, input, *args, **kwargs):
            try:
                if input == "":
                    if callable(self.update):
                        self.update(self)
                    output = self.code(self, input)
                    self.prev = output
                    self.mhist += output
                    return output
                self.ohist += input
                res = result(input, self.prev)
                self.score += res  # + 1
                self.round += 1
                if callable(self.update):
                    self.update(self)
                output = self.code(self, input)
                if self.shift % 3 == 2:
                    output = beat[beat[output]]
                elif self.shift % 3 == 1:
                    output = beat[output]
                self.prev = output
                self.mhist += output
                return output
            except Exception as e:
                print(self.name, self.round)
                raise e

        def metapredictors(self):
            pp = []
            mL = Predictor(self.code, self.update, self.setup, self.origname, 2)
            mW = Predictor(self.code, self.update, self.setup, self.origname, 1)
            pp = [mL, mW]
            return pp

        def __repr__(self):
            return self.name


    # Add Predictors
    predictors = []

    import random
    import math

    def decay(code, amt):
        def setup(self):
            setup.code(self)
            self.decay = setup.amt
        setup.code = code
        setup.amt = amt
        return setup

    def addpredictor(code, update = None, setup = None, name = "", mp = True, custom = {}):
        p = Predictor(code, update, setup, name)
        global predictors
        predictors.append(p)
        if mp:
            predictors += p.metapredictors()

    def random_(self, input):
        output = random.choice(["R", "P", "S"])
        return output

    addpredictor(random_, name = "random", mp = False)

    def wunrandomsetup(self):
        self.rockCount = self.paperCount = self.scissorsCount = 0

    def wunrandom(self, input):
        if input == "R":
            self.rockCount += 1
        elif input == "P":
            self.paperCount += 1
        elif input == "S":
            self.scissorsCount += 1
        if self.rockCount > self.paperCount and self.rockCount > self.scissorsCount:
            output = "P"  # paper beats rock
        elif self.paperCount > self.scissorsCount:
            output = "S"  # scissors beats paper
        else:
            output = "R"  # rock beats scissors (duh.)
        self.rockCount *= self.decay
        self.scissorsCount *= self.decay
        self.paperCount *= self.decay
        return output

    addpredictor(wunrandom, name = 'wrandom d1', setup = decay(wunrandomsetup, 0.9))  #, custom = {"decay": [1, 0.9, 0.75, 0.65, 0.5, 0.4]})
    addpredictor(wunrandom, name = 'wrandom d0.9', setup = decay(wunrandomsetup, 0.9))
    addpredictor(wunrandom, name = 'wrandom d0.75', setup = decay(wunrandomsetup, 0.75))
    addpredictor(wunrandom, name = 'wrandom d0.65', setup = decay(wunrandomsetup, 0.65))
    addpredictor(wunrandom, name = 'wrandom d0.5', setup = decay(wunrandomsetup, 0.5))
    addpredictor(wunrandom, name = 'wrandom d0.4', setup = decay(wunrandomsetup, 0.4))

    def wrandomsetup(self):
        self.rockCount = self.paperCount = self.scissorsCount = 0

    def wrandom(self, input):
        if input == "":
            return random.choice("RPS")
        elif input == "R":
            self.rockCount += 1
        elif input == "P":
            self.paperCount += 1
        elif input == "S":
            self.scissorsCount += 1

        # OLD:
        # output = beat[random.choice(list(self.ohist))]

        rnd = random.randrange(0, math.ceil(self.scissorsCount + self.paperCount + self.rockCount))
        if rnd < self.rockCount:
            output = "R"
        elif rnd < self.scissorsCount + self.rockCount:
            output = "S"
        else:
            output = "P"

        self.rockCount *= self.decay
        self.scissorsCount *= self.decay
        self.paperCount *= self.decay
        return beat[output]

    addpredictor(wrandom, name = 'wrandom d1', setup = decay(wrandomsetup, 1))  # , custom = {"decay": [1, 0.9, 0.75, 0.65, 0.5, 0.4]})
    addpredictor(wrandom, name = 'wrandom d0.9', setup = decay(wrandomsetup, 0.9))
    addpredictor(wrandom, name = 'wrandom d0.75', setup = decay(wrandomsetup, 0.75))
    addpredictor(wrandom, name = 'wrandom d0.65', setup = decay(wrandomsetup, 0.65))
    addpredictor(wrandom, name = 'wrandom d0.5', setup = decay(wrandomsetup, 0.5))
    addpredictor(wrandom, name = 'wrandom d0.4', setup = decay(wrandomsetup, 0.4))

    def nextmove(self, input):
        if input == '':
            output = random.choice("RPS")
        else:
            output = beat[input]
        return output

    addpredictor(nextmove, name = "nextmove")

    def histsearch(self, input):
        outputs = []
        if input == "":
            return random.choice("RPS")
        h = self.ohist
        for leng in range( 1, int(len(h) / 2) + 1 ):
            for s in range( 0, len(h) - leng ):
                str2 = h[s : leng + s]  # HELP OVER HERE PLZ PPLZ
                str1 = h[-leng : ]
                # print(leng, s, str1, str2, h)
                if str1 == str2:
                    outputs += h[leng + s]
        # print(outputs)
        if outputs:
            return beat[random.choice(outputs)]
        return random.choice("RPS")

    addpredictor(histsearch, name = "histsearch")

    bpcount = {}

# Main Wrapper
best = []
hscore = 0
for i in predictors:
    out = i(input)
    if i.score / i.round > hscore:
        best = []
    if i.score / i.round >= hscore:
        hscore = i.score / i.round
        best.append((i, out))

bp = random.choice(best)
output = bp[1]
if bp[0] in bpcount.keys():
    bpcount[bp[0]] += 1
else:
    bpcount[bp[0]] = 1

# if bp[0].round == 999:
#     for k, v in bpcount.items():
#         print(k + ": " + v)
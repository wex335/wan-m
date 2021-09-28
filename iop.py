def pr(text, effCodes=[]):
    code = ""
    for effcode in effCodes:
        setcolor(effcode)
    print(f"{text}\033[0m")


def p(text, effCodes=[]):
    code = ""
    for effcode in effCodes:
        setcolor(effcode)
    print(f"{text}", end="")


def setcolor(color):
    print(f"\033[{color}m", end="")


def move(x, y):
    print(f"\033[{x};{y}H", end="")


def movehor(x):
    print(f"\033[{x}G", end="")

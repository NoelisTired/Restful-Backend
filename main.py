import json, signal, readchar
def handler(signum, frame):
    print(msg := "[CTRL + C] was pressed, would you like to exit? (y/n)", end="", flush=True)
    res = readchar.readchar()
    if res.lower() == "y":
        print("")
        exit(1)
    else:
        print("", end="\r", flush=True)
        print(" " * len(msg), end="", flush=True) # clear the printed line
        print("    ", end="\r", flush=True)
def _clear():
    print("\033c", end="", flush=True)
    print("[NoelP X] - Loader")
    print("-" * 50)
if __name__ == "__main__":
    _clear()
    signal.signal(signal.SIGINT, handler)
    conf = json.load(open("./conf.json"))
    if conf["Api"]["Enabled"]:
        from routes import web
    if conf["Discord"]["Enabled"]:
        from routes import bot
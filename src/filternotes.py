import sys
import json

with open(sys.argv[1]) as f:
    flag = True
    for l in f:
        d = json.loads(l)
        if d["visibility"] in ["public", "home", "follower"]:
            print(d["id"])

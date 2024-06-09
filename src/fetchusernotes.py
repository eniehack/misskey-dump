import requests
import sys
import json
from argparse import ArgumentParser
from time import sleep


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--host")
    parser.add_argument("--user", "-u")
    args = parser.parse_args()

    payload = {
        "userId": args.user,
        "limit": 10,
    }

    while True:
        resp = requests.post(f"https://{args.host}/api/users/notes", json=payload)
        if resp.status_code != 200:
            print(f"status: {resp.status_code}", file=sys.stderr, flush=True)
            print(f"payload: {resp.json()}", file=sys.stderr, flush=True)
            break
        notes = resp.json()
        for note in notes:
            print(json.dumps(note, ensure_ascii=False), flush=True)
        if len(notes) != payload["limit"]:
            break
        payload["untilId"] = notes[-1]["id"]
        sleep(1)


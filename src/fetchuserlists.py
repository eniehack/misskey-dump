import requests
from argparse import ArgumentParser
import sys
import json


if __name__ == "__main__":
    cliparser = ArgumentParser()
    cliparser.add_argument("-i", "--token")
    cliparser.add_argument("--host")
    cliparser.add_argument("--local", default=True, type=bool)
    args = cliparser.parse_args()

    payload = {
      "limit": 10,
      "offset": 0,
      "sort": "+follower",
      "state": "all",
      "origin": "combined" if not args.local else "local",
      "username": None,
      "hostname": None,
    }
    headers = {
        "Authorization": f"Bearer {args.token}",
    }
    flag = True

    allUsers = []
    while flag:
        print("payload", payload, file=sys.stderr)
        resp = requests.post(f"https://{args.host}/api/admin/show-users", headers=headers, json=payload)
        if resp.status_code != 200:
            print(f"error: {resp.json()}", file=sys.stderr)
            break
        users = resp.json()
        allUsers.extend(users)
        if len(users) < payload["limit"]:
            flag = False
        else:
            payload["offset"] += payload["limit"]

    print(json.dumps(allUsers, ensure_ascii=False))

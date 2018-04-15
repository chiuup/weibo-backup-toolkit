import argparse
import json
import os
import random
import sys
import time

import requests


def fetch_container_id(uid):
    url = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s" % uid
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] == 1
    for tab in data["data"]["tabsInfo"]["tabs"]:
        if tab["tab_type"] == "weibo":
            container_id = tab["containerid"]
            break
    else:
        assert False

    return container_id


def fetch_page(base_url, n):
    url = (base_url + "&page=%s" % (n + 1)) if n else base_url
    response = requests.get(url)

    assert response.status_code == 200

    raw = response.content

    # A little hack ;)
    assert raw.startswith(b'{"ok":1')

    return raw


def main():
    parser = argparse.ArgumentParser(description="Dump your Weibo in json.")
    parser.add_argument("uid", type=int, help="Weibo UID")
    parser.add_argument("-n", default=0, type=int, help="Starting page")
    args = parser.parse_args()

    try:
        container_id = fetch_container_id(args.uid)
    except (AssertionError, KeyError):
        sys.stderr.write("Failed to fetch container ID.")
        exit(1)

    base_url = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=%s"
    base_url = base_url % (args.uid, container_id)

    user_path = "%s" % args.uid
    output_path = os.path.join(user_path, "raw")

    sys.stdout.write("Dumping to %s\n" %
                     os.path.join(os.getcwd(), output_path))

    if not os.path.exists(user_path):
        os.mkdir(user_path)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    n = args.n
    if n:
        sys.stdout.write("Resuming at page %s\n" % n)

    retry = 5

    while True:
        try:
            page = fetch_page(base_url, n)
        except AssertionError:
            sys.stderr.write("Busted. Taking a nap.\n")
            # Be even nicer to Weibo
            # TODO: Figure out a better way to terminate dumping. Or don't.
            time.sleep(5)
            if retry:
                retry -= 1
                continue
            else:
                sys.stdout.write("Dump terminated at page %s.\n" % (n-1))
                exit(0)

        with open(os.path.join(output_path, "page_%06d.json" % n), "wb+") as f:
            f.write(page)

        n += 1
        # Be nice to Weibo
        time.sleep(random.random())


if __name__ == "__main__":
    main()

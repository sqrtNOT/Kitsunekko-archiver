#!/usr/bin/python3
import requests
import time
import os
from bs4 import BeautifulSoup
import shutil

# create a directory to store the files
if not os.path.exists("kitsunekko"):
    os.mkdir("kitsunekko")
os.chdir("kitsunekko")

# seed the parser with a url
# accepts any of the dirlist.php urls
urls_todo = ["https://kitsunekko.net/dirlist.php?dir=subtitles%2Fjapanese%2F"]
download_links = []
request_wait = 5

# scrape urls recursively
while urls_todo:
    print("rate limiting for 5 seconds")
    time.sleep(request_wait)
    url = urls_todo.pop()
    print(f"processing url: {url}")
    ret = requests.get(url)
    soup = BeautifulSoup(ret.text, "html.parser")
    # use the fact that every page on kitsunekko presents files in the same table format
    for tag in soup.body.table.find_all("tr"):
        url = (tag.contents[0].contents[0]["href"]).lstrip("/")
        url = "https://www.kitsunekko.net/" + url
        if "dirlist" in url:
            urls_todo.append(url)
        else:
            download_links.append(url)

# prepare the directory structure to preserve the kitsunekko file hierarchy then download
for link in download_links:
    full_path = link.split("/")[5:]

    # skip previously downloaded files
    if os.path.exists("/".join(full_path)):
        continue

    # create directory structure
    for index in range(1, len(full_path)):
        partialpath = "/".join(full_path[0:index])
        if not os.path.exists(partialpath):
            os.mkdir(partialpath)

    # stream the download directly to a file
    with open("/".join(full_path), "wb") as f:
        print("rate limiting for 5 seconds")
        time.sleep(request_wait)
        print(f"Downloading new file: {'/'.join(full_path)}")
        with requests.get(link, stream=True) as r:
            shutil.copyfileobj(r.raw, f)

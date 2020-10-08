import os
import sys
import requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore



dir_name = sys.argv[1]
tags = ["p", "a", "ul", "ol", "li"]

if not os.path.exists(dir_name):
    os.mkdir(dir_name)
    print("{} created!".format(dir_name))
else:
     print(f"error Folder {dir_name} already exist")

history = deque()


def save_site_content(data, path):
    history.append(path)
    with open(os.path.join(dir_name, path), 'w') as f:
        f.write(data)


def get_site_content(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    # filtered_data = "\n".join([line.get_text().strip('\n |') for tag in tags for line in soup.find_all(tag)])
    # print(filtered_data)

    filtred_data = ''
    for tag in tags:
        for line in soup.find_all(tag):
            if tag == 'a':
                filtred_data += (Fore.BLUE + line.get_text().strip('\n |')) + '\n'
            else:
                filtred_data += line.get_text().strip('\n |')
    print(filtred_data)
    return(filtred_data)


def go_site(input_url):
    url = input_url if input_url.startswith("https://") else f"https://{input_url}"
    site_content = get_site_content(url)
    save_site_content(site_content, input_url)


def go_back():
    history.pop()
    with open(os.path.join(dir_name, history.pop())) as f:
        print(f.read())


while True:
    input_url = input()
    if input_url == "exit":
        break
    elif input_url == "back":
        go_back()
    elif '.' in input_url:
        go_site(input_url)
    else:
        print("Error: Incorrect URL")
import sys
import requests
import os
from pathlib import Path


def list():
    r = []
    f = [os.path.join(dirpath, f)
         for dirpath, dirnames, files in os.walk(os.getcwd())
         for f in files]
    for i in range(-1, len(f) - 1):
        s = str(f[i]).replace(str(os.getcwd()), '')
        s = s.replace('\\', '/')
        r.append(s[1:len(s)])
    return r


def download(url,name) :
    response = requests.get(url)
    #print(response.text)
    Path(name).write_bytes(response.content)


def existinserver(url) :
    #print(requests.get(url).status_code,url)
    if requests.get(url).status_code == 404 :
        return False
    else :
        return True
class options :
    ip = sys.argv[1]
    server_tree = eval(requests.get(f"http://{ip}:5000/list").text)
    server_ignore = eval(requests.get(f"http://{ip}:5000/ignore.txt").text)
    client_ignore = eval(open("ignore.txt").read())

incl = list()
for i in range(-1,len(incl)) :
    if not incl[i] in options.client_ignore :
        if not existinserver(f"http://{options.ip}:5000/{incl[i]}"):
            print(f"delete {incl[i]} because file is not existing in client side and is not in client whitelist (ignore.txt)")
            os.remove(incl[i])
        else :
            print(f"{incl[i]} exist in server")

for i in range(-1,len(options.server_tree)) :
    if not options.server_tree[i] in options.server_ignore :
        if os.path.exists(options.server_tree[i]) :
            if not requests.get(f"http://{options.ip}:5000/{options.server_tree[i]}").content == Path(options.server_tree[i]).read_bytes() :
                os.remove(options.server_tree[i])
                download(f"http://{options.ip}:5000/{options.server_tree[i]}",options.server_tree[i])
                print(f"downloading {options.server_tree[i]} because file is not in date")
            else :
                print(f"file {options.server_tree[i]} is in date")
        else :
            download(f"http://{options.ip}:5000/{options.server_tree[i]}", options.server_tree[i])
            print(f"downloading {options.server_tree[i]} because file is not existing in client side")


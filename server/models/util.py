from os import listdir
from os.path import isfile, join
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import pandas as pd
from . import config

def load_data():
    PATH = config.DATA_STORE
    contents = []
    files = [f"{PATH}{f}" for f in listdir(PATH) if isfile(join(PATH, f))]
    for file_path in files:
        with open(file_path, "rb") as f:
            byte_content = f.read()
            contents.append(byte_content.decode('utf-8', errors='ignore'))
    return files, contents


def load_stop_words(path: str = "../stopwords.txt"):
    words = []
    with open(path, "r") as f:
        words = f.read().split("\n")
    assert len(words) != 0, "no stop words were found"
    return words


def clean_html(contents:list) -> list:
    result = []
    for html in contents:
        soup = BeautifulSoup(html, 'html.parser')
        result.append(soup.get_text())
    return result

def clean_md(contents:list) -> list: 
    result = []
    numbers = "0123456789"
    non_acc_char = "\n,.()[]{}`/:-_*=\\<>|&%@?!\"'#" + numbers
    for doc in contents: 
        filtered = ""
        for word in doc.split(" "): 
            clean_word = ""
            for char in word: 
                if not char in non_acc_char:
                    clean_word += char
            if not "http" in clean_word:
                filtered += clean_word + " "
        result.append(filtered)
    return result

def clean(contents: list, remove_stop_words=True):
    if config.PARSE_HTML:
        contents = clean_html(contents)
    ascii_char = [chr(i) for i in range(0, 255)]
    numbers = "0123456789"
    non_acc_char = "\n,.()[]{}`/:-_*=\\<>|&%@?!\"'#" + numbers
    non_acc_tokens = ["https", "www", "com", "org", "license"]
    stop_words = [""] 
    if remove_stop_words: 
        stop_words = load_stop_words()
    for i, _ in enumerate(contents):
        for c in non_acc_char:
            contents[i] = contents[i].replace(c, " ")
        contents[i] = contents[i].split(" ")
        contents[i] = list(filter(lambda c: c != "", contents[i]))
        contents[i] = [t for t in contents[i] if not t in non_acc_tokens]
        contents[i] = [
            s.lower() for s in contents[i] if all(c in ascii_char for c in s)
        ]
        contents[i] = [t for t in contents[i] if not t in stop_words]
        for j, word in enumerate(contents[i]):
            if word[-1] == "s":
                contents[i][j] = word[:-1]
    return [" ".join(con) for con in contents]


def words_to_vec(words: str, labels: dict = {}):
    _words = words.split(" ")
    vec = []
    for word in _words:
        if word not in labels:
            labels[word] = len(labels)
        vec.append(labels[word])
    return vec, labels


def get_pid_from_cid(cid:str) -> str:
    df = pd.read_csv(config.META_DATA_STORE + "/week1/number_of_hosts.csv") # used number of hosts since it is short 
    pid = df[df["cid"] == cid]["peer"]
    if pid.to_list() == [] or pid.hasnans: 
        df = pd.read_csv(config.META_DATA_STORE + "/old/old_found.csv") # used number of hosts since it is short 
        pid = df[df["cid"] == cid]["peer"]
    if pid.to_list() == [] or pid.hasnans: return ""
    return pid.to_list()[0]
    
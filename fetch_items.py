#!/usr/bin/env python3

import os
import yaml
import requests
import json
from datetime import datetime
from typing import List, Tuple, Any, Union
from bs4 import BeautifulSoup

RTL_START = u'\u202B'
RTL_END = u'\u202C'

url = 'https://www.y net.co.il/news/category/184'.replace(" ", "")

# Load exclusion terms from file
_ = open("terms_to_exclude.txt", encoding="utf-8").read().split("\n")
_ = [term.strip() for term in _]
to_exclude = [term for term in _ if term != ""]


def is_skip(text: str, to_exclude: List[str]) -> bool:
    """
    Checks if the provided text should be skipped.
    Currently this is done by matching terms.

    Args:
        text (str): The input string to check.
        to_exclude (List[str]): A list of terms to exclude.

    Returns:
        bool: True if any term in `to_exclude` is found in `text`, False otherwise.
    """
    for t in to_exclude:
        if t in text:
            return True
    return False


def get_formated_headers_and_texts() -> Tuple[List[str], List[str]]:
    """
    Fetches news articles from the Ynet MIVZAKIM page, filters them by timestamp and exclusion terms,
    and formats their headers and texts.

    Returns:
        Tuple[List[str], List[str]]: A tuple of formatted headers and corresponding text content.
    """
    # 1. Get items
    time_stamps, headers, texts = fetch_items(url)

    # 2. Get last displayed time/date stamp
    last_seen_time_stamp = None
    if os.path.isfile("last_seen_time_stamp.yaml"):
        last_seen_time_stamp_str = yaml.safe_load(open("last_seen_time_stamp.yaml"))
        _ = last_seen_time_stamp_str.replace('Z', '+00:00')
        last_seen_time_stamp = datetime.fromisoformat(_)

    # 3. Get the headers+texts not-skipped by keywork + more recent than time stamp
    formated_headers =  []
    formated_texts = []
    for i in range(len(time_stamps) - 1, -1, -1):
        time_stamp = datetime.fromisoformat(time_stamps[i].replace('Z', '+00:00'))
        if last_seen_time_stamp and time_stamp < last_seen_time_stamp:
            continue
        if is_skip(headers[i], to_exclude):
            continue
        local_time = time_stamp.astimezone()
        time_stamp_disp = local_time.strftime("%d%b %H:%M")
        header = RTL_START + headers[i] + RTL_END
        formated_headers.append(str(i + 1).rjust(2) + " " + time_stamp_disp + " " + header)
        formated_texts.append(texts[i])

    formated_headers.append(f'Fetched: {datetime.now().strftime("%d%b %H:%M")}')
    formated_texts.append("")

    # 4. Save time stamp
    if os.path.isfile("last_seen_time_stamp.yaml"):
        os.rename("last_seen_time_stamp.yaml", "previous_time_stamp.yaml")
    yaml.safe_dump(time_stamps[0], open("last_seen_time_stamp.yaml", 'w'))

    return formated_headers, formated_texts


def html_to_dict(url: str) -> dict:
    """
    Converts the HTML structure of the given URL into a nested dictionary representation.

    Args:
        url (str): URL of the webpage to convert.

    Returns:
        dict: A dictionary representation of the HTML structure.
    """
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    def parse_tag(tag: Any) -> dict:
        tag_dict = {'tag': tag.name}
        if tag.attrs:
            tag_dict['attributes'] = tag.attrs
        if tag.string:
            tag_dict['text'] = tag.string.strip()

        children = []
        for child in tag.children:
            if isinstance(child, str):
                continue
            children.append(parse_tag(child))

        if children:
            tag_dict['children'] = children

        return tag_dict

    return parse_tag(soup)


def interactive_explorer_of_data_struct(d: Any, l: int, path: List[str]) -> None:
    """
    Allows interactive exploration of a nested data structure (HTML parsed as dicts/lists).
    This code is used for exploration of the page strcture and is not in use during normal runs.
    Args:
        d (Any): The current element of the data structure.
        l (int): Current depth level.
        path (List[str]): Path to the current element.
    """
    path_printable = ", ".join(path)
    type_of_d = str(type(d)).split("'")[1]

    match type_of_d:
        case "str" | "int":
            print(f"   '{d}'")
        case "list":
            def get_ans(d: list) -> str:
                print(f'Level {l}. type {type_of_d}. Path {path_printable}')
                print("   len", len(d))
                for i, item in enumerate(d):
                    if type(item)==type({}):
                        if "tag" in item.keys():
                            print("   ", i + 1, item["tag"], len(str(item)))
                return input("num of element (start w/1) or 'Enter' to return > ")

            ans = get_ans(d)
            while ans != '':
                new_path = path + [str(int(ans) - 1)]
                interactive_explorer_of_data_struct(d[int(ans) - 1], l + 1, new_path)
                ans = get_ans(d)

        case "dict":
            def get_ans(keys: List[str]) -> str:
                print(f'Level {l}. type {type_of_d}. Path {path_printable}')
                print("keys:")
                for idx, key in enumerate(keys):
                    print("   ", idx + 1, key)
                return input("p to print, num of key or 'Enter' to return > ")

            keys = list(d.keys())
            if "tag" in keys and isinstance(d["tag"], str):
                print("   Tag:", d["tag"])
                keys.remove("tag")

            ans = get_ans(keys)
            while ans != "":
                match ans:
                    case "p":
                        print(d)
                    case _:
                        key = keys[int(ans) - 1]
                        new_path = path + [f'"{key}"']
                        interactive_explorer_of_data_struct(d[key], l + 1, new_path)
                ans = get_ans(keys)

        case _:
            print("Unknown type:", type_of_d)


def fetch_items(url: str) -> Tuple[List[str], List[str], List[str]]:
    """
    Fetches article data from a structured Ynet HTML page, extracts the timestamp, title, and text fields.

    Args:
        url (str): The URL to fetch the HTML from.

    Returns:
        Tuple[List[str], List[str], List[str]]: Lists of timestamps, headers, and article texts.
    """
    html_dict = html_to_dict(url)

    path = [
        "children", 0, "children", 1, "children", 14, "children", 0,
        "children", 0, "children", 5, "children", 0, "children", 4,
        "children", 0, "children", 0, "children", 0, "children", 0,
        "children", 1, "text"
    ]

    for p in path:
        try:
            html_dict = html_dict[p]
        except:
            print(f"ERROR: could not get {p} from html_dict.")
            print("html_dict:", html_dict)
            exit()

    ### Uncomment the below two lines to do manual exploration of the path
    #interactive_explorer_of_data_struct(html_dict, 0, [])
    #exit()

    items = html_dict.split("items")[1][2:-2]
    items = items.split("isLTR")[0][:-2]
    items = json.loads(items)

    time_stamps, headers, texts = [], [], []

    for item in items:
        try:
            time_stamps.append(item["date"])
        except:
            print("Getting time stamp failed")
        try:
            headers.append(item["title"])
        except:
            print("Failed to get title")
        try:
            texts.append(item["text"])
        except:
            print("Failed to get text")

    return time_stamps, headers, texts

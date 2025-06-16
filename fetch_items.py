#!/usr/bin/env python3

import requests, json
from bs4 import BeautifulSoup
RTL_START = u'\u202B'
RTL_END = u'\u202C'



def html_to_dict(url):
    # Fetch the HTML content from the URL
    response = requests.get(url)
    html_content = response.text
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # Define a helper function to convert tags into a dictionary
    def parse_tag(tag):
        tag_dict = {}
        # Extract the tag name
        tag_dict['tag'] = tag.name
        # Extract attributes, if any
        if tag.attrs:
            tag_dict['attributes'] = tag.attrs
        
        # Extract text content, if any
        if tag.string:
            tag_dict['text'] = tag.string.strip()
        
        # Recurse into child tags (if any)
        children = []
        for child in tag.children:
            if isinstance(child, str):
                continue  # Skip string nodes (text content)
            children.append(parse_tag(child))
        
        if children:
            tag_dict['children'] = children
        
        return tag_dict
    # Convert the entire document (or specific part) to a dictionary
    root_dict = parse_tag(soup)
    return root_dict



def interactive_explorer_of_data_struct(d, l, path):
    # Interactivly explore HTML page that was converted to Python dicts/list Hybrid
    path_printable = ", ".join(path)
    type_of_d = str(type(d)).split("'")[1]
    match type_of_d:
        case "str" | "int":
           print(f"   '{d}'")
        case "list":
           def get_ans(d):
               print(f'Level {l}. type {type_of_d}. Path {path_printable}')
               print("   len", len(d))
               for i, item in enumerate(d):
                   if type(item)==type({}):
                       if "tag" in item.keys():
                           print("   ", i+1, d[i]["tag"], len(str(d[i])))
               return input("num of element (start w/1) or 'Enter' to return > ")
           ans = get_ans(d)
           while ans!='': 
               new_path = path + [str(int(ans)-1)]
               interactive_explorer_of_data_struct(d[int(ans)-1], l+1, new_path)
               ans = get_ans(d)
        case "dict":
           def get_ans(keys):
               print(f'Level {l}. type {type_of_d}. Path {", ".join(path)}')
               print("keys:") 
               for idx, key in enumerate(keys):
                   print("   ", idx+1, key)
               return input("p to print, num of key or 'Enter' to return > ")

           keys = list(d.keys())
           if "tag" in keys:
              if type(d["tag"])==type(""):
                  print("   Tag:", d["tag"])
                  keys.remove("tag")
           ans = get_ans(keys)
           E
           while ans!="":
               match ans:
                  case "p":
                     print(d)
                  case _:
                      key = keys[int(ans)-1]
                      new_path = path + ['"'+key+'"']
                      interactive_explorer_of_data_struct(d[key], l+1, new_path)
               ans = get_ans(keys)
        case _:
           print("Unknown type:", type_of_d)

def fetch_items(url):
    html_dict = html_to_dict(url)
    path  = ["children", 0, "children", 1, "children", 14, "children", 0]
    path += ["children", 0, "children", 5, "children", 0, "children", 4 ]
    path += ["children", 0, "children", 0, "children", 0, "children", 0 ]
    path += [ "children", 1, "text"]

    for p in path:
        # print("      ", p)
        try:
            html_dict = html_dict[p]
        except:
            print(f"ERROR: could not get {p} from html_dict.")
            print("html_dict:", html_dict)
            exit()
    #interactive_explorer_of_data_struct(html_dict, 0, [])
    #exit()

    items = html_dict.split("items")[1][2:-2]
    items = items.split("isLTR")[0][:-2]

    items = json.loads(items)

    time_stamps = []
    headers = []
    texts = []
    for idx, item in enumerate(items):
        try:
            time_stamp = item["date"]
            time_stamps.append(time_stamp)
        except:
            print("Getting time stamp failed")
        try:
            header = item["title"]
            headers.append(header)
        except:
            print("Failed")
        try:
            text = item["text"]
            texts.append(text)
        except:
            print("Failed")
    return time_stamps, headers, texts


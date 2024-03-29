import csv
import collections
import json
import os

from typing import Dict

CATEGORY_NAME_DEFAULT = "Default"

input_filename = "locale/en.json"
output_directory = "template"


category_dict: Dict[str, list] = collections.defaultdict(list)

with open(input_filename, "r", encoding="utf-8") as f:
    j = json.load(f)

for key, src in j.items():
    parts = key.split('/&', maxsplit=1)

    if len(parts) == 2:
        category = parts[0]
    else:
        category = CATEGORY_NAME_DEFAULT
    
    if category == "Credits":
        continue
    
    category_dict[category].append((key, src))

counts = [(k, len(v)) for k, v in category_dict.items()]
counts.sort(key=lambda x: x[1], reverse=True)

for name, strings in list(category_dict.items()):
    if len(strings) < 20:
        category_dict[CATEGORY_NAME_DEFAULT].extend(strings)
        del(category_dict[name])

os.makedirs(output_directory, exist_ok=True)

for name, strings in category_dict.items():
    print(name, len(strings))
    with open(os.path.join(output_directory, f"{name}.csv"), "w", encoding="utf-8", newline="") as of:
        w = csv.writer(of, quoting=csv.QUOTE_ALL)
        w.writerow(["context", "source", "target"])
        w.writerows(strings)

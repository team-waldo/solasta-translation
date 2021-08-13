import csv
import collections
import os

from typing import Dict

CATEGORY_NAME_DEFAULT = "Default"

input_filename = "en.csv"
output_directory = "template"


category_dict: Dict[str, list] = collections.defaultdict(list)

with open(input_filename, "r", encoding="utf-8") as f:
    r = csv.reader(f)
    header = next(r)
    data = list(r)

for row in data:
    parts = row[0].split('/&', maxsplit=1)
    key = parts[-1]
    if len(parts) == 2:
        category = parts[0]
    else:
        category = CATEGORY_NAME_DEFAULT
    
    if category == "Credits":
        continue
    
    source = row[1]
    category_dict[category].append((key, source))

counts = [(k, len(v)) for k, v in category_dict.items()]
counts.sort(key=lambda x: x[1], reverse=True)

for name, strings in list(category_dict.items()):
    if len(strings) < 20:
        category_dict[CATEGORY_NAME_DEFAULT].extend(strings)
        del(category_dict[name])

os.makedirs(output_directory, exist_ok=True)

for name, strings in category_dict.items():
    with open(os.path.join(output_directory, f"{name}.csv"), "w", encoding="utf-8", newline="") as of:
        w = csv.writer(of, quoting=csv.QUOTE_ALL)
        w.writerow(["context", "source", "target"])
        w.writerows(strings)

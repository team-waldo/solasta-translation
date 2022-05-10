import glob

from translation import TranslationEntry, TranslationFile


chars = set()

with open("base_glyphs.txt", "r", encoding="utf-8") as f:
    chars.update(f.read())

backup = chars.copy()

for fpath in glob.glob("translation/ko/*.po"):
    print(fpath)
    tf = TranslationFile(fpath)
    
    for entry in tf:
        for ch in entry.target:
            chars.add(ch)

chars_list = list(chars)
chars_list.sort()

chars_str = "".join(chars_list)

added = chars.difference(backup)
print(added)

with open("font_chars.txt", "w", encoding="utf-8") as f:
    f.write(chars_str)

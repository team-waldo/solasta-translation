import glob

from translation import TranslationEntry, TranslationFile


chars = set()

for fpath in glob.glob("translation/ko/*.po"):
    print(fpath)
    tf = TranslationFile(fpath)
    
    for entry in tf:
        for ch in entry.target:
            chars.add(ch)

chars_list = list(chars)
chars_list.sort()

print("".join(chars_list))

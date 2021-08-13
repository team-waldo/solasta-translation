import csv
import os
from translation import TranslationFile


TRANSLATION_BASE_DIRECTORY = "translation"
MACHINETRANSLATION_SUFFIX = "_mt"


def read_csv(csv_path: str):
    with open(csv_path, "r", encoding="utf-8") as f:
        r = csv.reader(f)
        _header = next(r)
        rows = list(r)
    return rows


def read_file(path: str):
    name = os.path.splitext(os.path.basename(path))[0]
    f = TranslationFile(path)
    return {f"{name}/&{x.key}": x.target for x in f if x.target}


def read_directory(path: str):
    result = {}

    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        result.update(read_file(filepath))

    return result


def get_translation(dictionary: dict, key: str):
    if tr := dictionary.get(key, None):
        return tr

    name = key.split("/&", 1)[-1]
    key = f"Default/&{name}"

    return dictionary.get(key, None)


def escape(s: str):
    return s.replace("\n", "\\n").replace("\r", "\\r")


def translate_locale(locale, dictionary, output_path):
    tsv_data = []

    for row in locale:
        if not row:
            continue
        key, source = row[:2]
        if tr := get_translation(dictionary, key):
            tsv_data.append([key, escape(tr)])

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        for key, text in tsv_data:
            f.write(f"{key}\t{text}\n")


def main():
    langcode = "ko"

    tr_dir = os.path.join(TRANSLATION_BASE_DIRECTORY, langcode)
    mt_dir = os.path.join(TRANSLATION_BASE_DIRECTORY, langcode + MACHINETRANSLATION_SUFFIX)

    tr = read_directory(tr_dir)
    mt = read_directory(mt_dir)
    mt.update(tr)

    locale = read_csv("locale/en.csv")

    os.makedirs("output", exist_ok=True)

    translate_locale(locale, tr, f"output/{langcode}.txt")
    translate_locale(locale, mt, f"output/{langcode}{MACHINETRANSLATION_SUFFIX}.txt")


if __name__ == '__main__':
    main()

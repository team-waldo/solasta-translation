import csv
import os

from translation import TranslationFile, TranslationEntry


TEMPLATE_DIRECTORY = "template"
TRANSLATION_DIRECTORY = "translation"
MACHINETRANSLATION_SUFFIX = "_mt"


class Translation:
    context: str
    fuzzy: bool
    source: str
    target: str
    prev_source: str


def read_csv(csv_path: str):
    with open(csv_path, "r", encoding="utf-8") as f:
        r = csv.reader(f)
        _header = next(r)
        rows = list(r)
    return rows


def merge(template_data, translation_path):
    template = TranslationFile()
    for key, source in template_data:
        template.append(TranslationEntry(key=key, source=source))

    path = translation_path if os.path.isfile(translation_path) else None
    tr = TranslationFile(path)

    if len(tr) != 0:
        merged = template.merge(tr)
        if merged:
            template.export(translation_path)


def update(filename, langcode):
    template_path = os.path.join(TEMPLATE_DIRECTORY, filename)
    template_data = read_csv(template_path)

    po_name = os.path.splitext(filename)[0] + ".po"

    translation_path = os.path.join(TRANSLATION_DIRECTORY, langcode, po_name)
    merge(template_data, translation_path)


def main():
    langcode = "ko"

    os.makedirs(os.path.join(TRANSLATION_DIRECTORY, langcode), exist_ok=True)

    for filename in os.listdir(TEMPLATE_DIRECTORY):
        if not filename.endswith("csv"):
            continue
        update(filename, langcode)


if __name__ == '__main__':
    main()

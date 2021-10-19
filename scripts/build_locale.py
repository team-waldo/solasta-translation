import datetime
import json
import os
from translation import TranslationFile


TRANSLATION_BASE_DIRECTORY = "translation"


def read_file(path: str):
    name = os.path.splitext(os.path.basename(path))[0]
    f = TranslationFile(path)
    return {x.key: x.target for x in f if x.target}


def read_directory(path: str):
    result = {}

    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        result.update(read_file(filepath))

    return result


def main():
    langcode = "ko"

    tr_dir = os.path.join(TRANSLATION_BASE_DIRECTORY, langcode)

    tr = read_directory(tr_dir)

    json_data = {
        "creation_date": str(datetime.datetime.utcnow().isoformat()),
        "strings": tr,
    }

    with open("translation.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()

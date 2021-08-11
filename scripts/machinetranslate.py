import os

from deep_translator import GoogleTranslator

from translation import TranslationEntry, TranslationFile

from tqdm import tqdm


OUTPUT_FOLDER = "Translations-"
CHARS_MAX = 4999
SEPARATOR = "\x0D"


class MachineTranslator:
    def __init__(self, target: str):
        self.translator = GoogleTranslator(source="en", target=target)

    def translate_list(self, lst: list[TranslationEntry]):
        joined = "\r\n".join(x.source for x in lst)
        result = self.translator.translate(joined).split("\r\n")
        for entry, tr in zip(lst, result):
            entry.target = tr

    def translate_file(self, file: TranslationFile):
        print(f"Translating {len(file)} strings...")
        count = 0
        lst = []
        entry: TranslationEntry
        for entry in tqdm(file):
            if not entry.fuzzy and entry.target:
                continue

            length = len(entry.source)
            if length > CHARS_MAX:
                continue

            if count + length > CHARS_MAX:
                self.translate_list(lst)
                lst.clear()
                count = 0
            lst.append(entry)
            count += length + 2  # for \r\n

        if lst:
            self.translate_list(lst)

        print("Done")


def main():
    mt = MachineTranslator("ko")
    target_dir = "translation/ko_mt/"

    files = list(os.listdir(target_dir))

    for i, filename in enumerate(files):
        print()
        print(filename)
        path = os.path.join(target_dir, filename)
        tf = TranslationFile(path)

        mt.translate_file(tf)
        tf.export(path)


if __name__ == '__main__':
    main()
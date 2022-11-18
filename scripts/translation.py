from typing import List

from translate.storage import pypo


class TranslationEntry:
    """
    Wrapper class to help working with translate.storage.pypo
    """
    def __init__(self, key: str, source: str, comment: str = "", prev_source: str = "", target: str = "",
                 location: str = "", fuzzy: bool = False) -> None:
        self.key = key
        self.source = source
        self.comment = comment
        self.prev_source = prev_source
        self.target = target
        self.location = location
        self.fuzzy = fuzzy

    @classmethod
    def from_pounit(cls, pounit: pypo.pounit) -> "TranslationEntry":
        comment = "\n".join(pounit.getnotes("developer"))
        location = "\n".join(pounit.getlocations())
        entry = cls(
            key=pounit.getcontext(),
            source=pounit.source,
            comment=comment,
            prev_source=pounit.prev_source,
            target=pounit.target,
            location=location,
            fuzzy=pounit.isfuzzy()
        )
        return entry

    def to_pounit(self) -> pypo.pounit:
        unit = pypo.pounit(source=self.source)
        unit.setcontext(self.key)
        if self.comment:
            for line in self.comment.split("\n"):
                unit.addnote(line, "developer")
        unit.prev_source = self.prev_source
        unit.target = self.target
        if self.location:
            for line in self.location.split("\n"):
                unit.addlocation(line)
        unit.markfuzzy(self.fuzzy)
        return unit

    def __repr__(self) -> str:
        return f"[{self.key}] {self.source}:{self.target}"


class TranslationFile(List[TranslationEntry]):
    def __init__(self, path: str = None) -> None:
        super().__init__()
        if not path:
            return

        with open(path, "rb") as f:
            po = pypo.pofile(f)

        for pounit in po.unit_iter():
            entry = TranslationEntry.from_pounit(pounit)
            self.append(entry)

    def export(self, path: str) -> None:
        po = pypo.pofile()

        for entry in self:
            po.addunit(entry.to_pounit())

        with open(path, "wb") as f:
            po.savefile(f)

    def merge(self, origin: "TranslationFile") -> bool:
        updated = False
        origin_dict = {e.key: e for e in origin}
        for entry in self:
            old_entry = origin_dict.get(entry.key, None)
            if not old_entry:
                updated = True
                continue
            if not old_entry.target:
                continue
            if old_entry.source != entry.source:
                entry.prev_source = old_entry.source
                entry.fuzzy = True
                updated = True
            entry.target = old_entry.target
        return updated

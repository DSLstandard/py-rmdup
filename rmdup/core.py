from dataclasses import dataclass
from pathlib import Path
from typing import *
import collections
import hashlib
import natsort
import os

__all__ = [
    "Entry",
    "iter_entries",
    "find_directories",
    ]

def hash_file(path: Path, chunk_size: int = 1048576) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as f:
        sha.update(f.read(chunk_size))
    return sha.hexdigest()

@dataclass
class Entry:
    main: Path
    duplicates: list[Path]

    def is_unique(self) -> bool:
        return len(self.duplicates) == 0

def iter_entries(dir_path: Path, yield_uniques: bool = False) -> Iterator[Entry]:
    assert dir_path.is_dir()

    # find sets of files with equal content
    eq_sets = collections.defaultdict(lambda: [])
    for file_path in dir_path.iterdir():
        if not file_path.is_file():
            continue # skip non-files
        key = hash_file(file_path)
        eq_sets[key].append(file_path)

    # yield entries
    for file_paths in eq_sets.values():
        file_paths = natsort.os_sorted(file_paths, key=lambda path: path.name)
        entry = Entry(main=file_paths[0], duplicates=file_paths[1:])

        if not (entry.is_unique() and not yield_uniques):
            yield entry

def find_directories(start_path: Path) -> Iterator[Path]:
    for dir_path, _, _ in os.walk(str(start_path)):
        yield Path(dir_path)

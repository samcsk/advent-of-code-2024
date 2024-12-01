from pathlib import Path
from typing import Tuple


def lists_from_file(file: Path) -> Tuple[list[int], ...]:
    with open(file=file, mode="r") as f:
        lines: list[str] = f.readlines()
        la = zip(*[line.split() for line in lines])
        return tuple(list(map(int, li)) for li in la)


def _calculate_distance(a: list[int], b: list[int]) -> int:
    a.sort()
    b.sort()
    return sum([abs(a_i - b[idx]) for idx, a_i in enumerate(a)])


def calculate_distance(file: Path) -> int:
    return _calculate_distance(*lists_from_file(file))


def _calculate_similarity(a: list[int], b: list[int]) -> int:
    return sum([a_i * b.count(a_i) for a_i in a])


def calculate_similarity(file: Path) -> int:
    return _calculate_similarity(*lists_from_file(file))


def calculate(file: Path) -> Tuple[int, int]:
    return calculate_distance(file), calculate_similarity(file)


if __name__ == "__main__":
    assert calculate(Path("sample.txt")) == (11, 31)
    print(calculate(Path("input.txt")))

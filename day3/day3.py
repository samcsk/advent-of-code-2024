from pathlib import Path
import re
from typing import Tuple


def string_from_file(file: Path) -> str:
    with open(file, "r"):
        return file.read_text()


def get_multiplications_from(input: str, part2: bool = False) -> list[Tuple[int, ...]]:
    doers_pat = re.compile(r"do\(\)(.*?)don't\(\)", flags=re.DOTALL)
    pat = re.compile(r"mul\((\d+),(\d+)\)")

    results = []
    matches = doers_pat.findall(f"do(){input.strip()}don't()")
    for match in matches if part2 else [input]:
        results.extend([tuple(map(int, result)) for result in pat.findall(match)])
    return results


def process(input: str, part2: bool = False) -> int:
    mults = get_multiplications_from(input, part2)
    sum = 0
    for mult in mults:
        sum += mult[0] * mult[1]
    return sum


def calculate(file: Path, part2: bool = False) -> int:
    return process(string_from_file(file), part2)


if __name__ == "__main__":
    assert calculate(Path("sample.txt")) == 161
    print(calculate(Path("input.txt")))
    assert calculate(Path("sample2.txt"), part2=True) == 48
    print(calculate(Path("input_2.txt"), part2=True))

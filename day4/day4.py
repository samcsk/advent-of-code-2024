from pathlib import Path
from typing import NamedTuple, Self


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, val2: Self) -> "Point":
        return Point(self.x + val2.x, self.y + val2.y)

    def __mul__(self, val: int):
        return Point(self.x * val, self.y * val)


def list_from_file(file: Path) -> list[str]:
    with open(file=file, mode="r") as f:
        lines: list[str] = [line.strip() for line in f.readlines()]
        return lines


def find_letters_in_array(
    array: list[str], letters: dict[str, list]
) -> dict[str, list]:
    for letter in letters.keys():
        if len(letter) != 1:
            raise TypeError("letter must be of length 1")
    for y, row in enumerate(array):
        for x, _letter in enumerate(row):
            if _letter in letters.keys():
                letters[_letter].append(Point(x=x, y=y))
    return letters


def findx(array: list[str], query: str) -> int:
    if len(query) % 2 == 0:
        raise ValueError("Finding X-shape only works for odd number of characters.")

    OFFSETS = [Point(_x, _y) for _y in [-1, 1] for _x in [-1, 1]]
    limit = Point(x=len(array[0]) - 1, y=len(array) - 1)
    locations: dict[str, list[Point]] = find_letters_in_array(
        array, {letter: [] for letter in query}
    )

    found = []

    mid_idx = int(len(query) / 2)
    mid_char = query[mid_idx]

    for starting_point in locations[mid_char]:
        res = [starting_point]
        if any(
            [
                ((max := starting_point + offset * mid_idx).x > limit.x)
                or (max.y > limit.y)
                or (max.x < 0)
                or (max.y < 0)
                for offset in OFFSETS
            ]
        ):
            # Out of bound
            continue
        for ringidx in range(1, mid_idx + 1):
            next_points = {
                offset: starting_point + offset * ringidx for offset in OFFSETS
            }
            ring = {
                offset: char_type
                for char_type, _list in enumerate(
                    [
                        locations[query[mid_idx - ringidx]],
                        locations[query[mid_idx + ringidx]],
                    ]
                )
                for offset, point in next_points.items()
                if point in _list
            }
            if len(ring) != (len(query) - 1) * 2:
                break
            """
            Consider:
            M.S  S.M  M.M  S.S |     S.M
            .A.  .A.  .A.  .A. | and .A.
            M.S  S.M  S.S  M.M |     M.S
            in no condition shall there be diagonal letters in the same ring having
            the same character.
            """
            if (
                ring[Point(-1, -1)] == ring[Point(1, 1)]
                or ring[Point(1, -1)] == ring[Point(-1, 1)]
            ):
                break
            res.extend(next_points.values())
        else:
            print(f"Found X: {res}")
            found.append(res)
    return len(found)


def find(array: list[str], query: str) -> int:
    OFFSETS = [
        Point(_x, _y) for _y in [-1, 0, 1] for _x in [-1, 0, 1] if (_x, _y) != [0, 0]
    ]

    limit = Point(x=len(array[0]) - 1, y=len(array) - 1)
    locations: dict[str, list[Point]] = find_letters_in_array(
        array, {letter: [] for letter in query}
    )

    found = []

    for starting_point in locations[query[0]]:
        for offset in OFFSETS:
            res = [starting_point]
            max = starting_point + offset * (len(query) - 1)
            if (max.x > limit.x) or (max.y > limit.y) or (max.x < 0) or (max.y < 0):
                # Out of bound
                continue
            for i in range(1, len(query)):
                next_point = starting_point + offset * i
                if next_point not in locations[query[i]]:
                    break
                else:
                    res.append(next_point)
            if len(res) == len(query):
                print(f"Found: {res}")
                found.append(res)
    return len(found)


def calculate(file: Path, query: str, part2: bool = False) -> int:
    fn = find if not part2 else findx
    return fn(list_from_file(file), query)


if __name__ == "__main__":
    QUERY = "XMAS"
    assert calculate(Path("sample.txt"), QUERY) == 18
    print(calculate(Path("input.txt"), QUERY))

    QUERY_X = QUERY[1:]
    assert calculate(Path("sample.txt"), QUERY_X, part2=True) == 9
    print(calculate(Path("input.txt"), QUERY_X, part2=True))

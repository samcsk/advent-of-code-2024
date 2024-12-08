from pathlib import Path


def file_parse(file: Path) -> tuple[list[tuple[int, ...]], list[list[int]]]:
    with open(file=file, mode="r") as f:
        lines: list[str] = [line.strip() for line in f.readlines()]
    rules: list[tuple[int, ...]] = []
    updates: list[list[int]] = []
    for line in lines:
        if "|" in line:
            rules.append(tuple(map(int, line.split("|"))))
        elif "," in line:
            updates.append(list(map(int, line.split(","))))
    return rules, updates


def process(rules: list[tuple[int, ...]], updates: list[list[int]]) -> tuple[int, int]:
    _rules: dict[int, list[int]] = {}
    for before, after in rules:
        if before in _rules:
            _rules[before].append(after)
        else:
            _rules[before] = [after]

    # Part 1
    updates_correct: list[list[int]] = []
    updates_needs_fixing: list[list[int]] = []
    for update in updates:
        for idx, page in enumerate(update):
            if idx == 0:
                continue
            if page not in [
                page
                for i in range(len(update) - idx + 1)
                if update[idx - i] in _rules
                for page in _rules[update[idx - i]]
            ]:
                updates_needs_fixing.append(update)
                break
        else:
            updates_correct.append(update)
    sum_correct = sum([_res[int(len(_res) / 2)] for _res in updates_correct])

    # Part 2
    fixed = []
    for update in updates_needs_fixing:
        mapper = {
            page: [p for p in _rules[page] if p in update]
            for page in update
            if page in _rules
        }
        mapper.update({page: [] for page in update if page not in mapper})
        _sorted = [
            s[0] for s in sorted(mapper.items(), key=lambda x: len(x[1]), reverse=True)
        ]
        fixed.append(_sorted)
    sum_fixed = sum([_res[int(len(_res) / 2)] for _res in fixed])
    return sum_correct, sum_fixed


def calculate(file: Path) -> tuple[int, int]:
    return process(*file_parse(file))


if __name__ == "__main__":
    assert calculate(Path("sample.txt")) == (143, 123)
    print(calculate(Path("input.txt")))

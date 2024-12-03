from pathlib import Path


def list_from_file(file: Path) -> list[list[int]]:
    with open(file=file, mode="r") as f:
        lines: list[str] = f.readlines()
        la = [[int(e) for e in line.split()] for line in lines]
        return la


def is_report_safe(report: list[int], extra_chance: bool = False) -> bool:
    last_diff = 0
    for idx, _ in enumerate(report):
        if idx == (len(report) - 1):
            # Only len(report) - 1 comparisons has to be made
            return True
        _diff = report[idx + 1] - report[idx]
        if (abs(_diff) not in range(1, 4)) or (
            last_diff and ((last_diff > 0) != (_diff > 0))
        ):
            if extra_chance:
                for i in range(len(report)):
                    _report = report.copy()
                    _report.pop(i)
                    if is_report_safe(_report):
                        return True
            return False
        last_diff = _diff
    return True


def count_safe_reports(reports: list[list[int]], extra_chance: bool = False) -> int:
    count = 0
    for report in reports:
        if is_report_safe(report, extra_chance):
            count += 1
    return count


def calculate(file: Path) -> tuple[int, int]:
    return (
        count_safe_reports(list_from_file(file)),
        count_safe_reports(list_from_file(file), extra_chance=True),
    )


if __name__ == "__main__":
    assert calculate(Path("sample.txt")) == (2, 4)
    print(calculate(Path("input.txt")))

#!/bin/env python3

from typing import List, Tuple

def main() -> int:
    delim: str = ','
    raw: str = input("Enter numbers: ")
    try:
        list: List[int] = [int(i) for i in raw.strip(delim).split(delim)]
    except ValueError as e:
        print(f"{e}\nPlease, only enter valid numbers.")
        return 1
    tup: Tuple[int, ...] = tuple(list)
    print(f"Output:\n{list=}\n{tup=}")
    return 0


if __name__ == "__main__":
    exit(main())

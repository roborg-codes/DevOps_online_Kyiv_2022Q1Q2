#!/bin/env python3

from typing import List
from os import path

def main() -> int:
    fname: str = input("Please enter filename: ")
    if not path.exists(fname):
        print("File does not exist.")
        return 1
    with open(fname, 'r') as file:
        content: List[str] = file.readlines()
        [print(l) for l in content[1::2]]
    return 0


if __name__ == "__main__":
    exit(main())

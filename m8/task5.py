#!/bin/env python3

from sys import argv
from typing import List

from emoji import emojize

def main(args: List[str]) -> int:
    for arg_text in args[1:]:
        try:
            print(
                emojize(
                    arg_text,
                    delimiters=(' ', ' '),
                    language='alias',
                    variant='text_type'
                )
            )
        except ValueError as e:
            print(f"Error: {e}")
            return 1

    return 0

if __name__ == "__main__":
    exit(main(argv))

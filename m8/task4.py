#!/bin/env python

from lxml.html import parse


def main() -> int:
    doc: str = input("Please enter document to parse: ")
    try:
        doc = parse(doc).getroot()
    except OSError as e:
        print(f"{e}\nDocument does not exist.")
        return 1
    [print(t.text_content()) for t in doc.cssselect('title')]
    return 0


if __name__ == "__main__":
    exit(main())

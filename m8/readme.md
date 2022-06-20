# Python

* note: all programs are located in the same 'directory' as this readme file.

## 1

For this task a simple builtin module sufficed:

```python
from datetime import datetime as dt

print(f"Current date and time: {dt.today()}")
```

## 2

Task 2 program accepts input as a string of text from the user, then separates and splits it on commas, and turns them into instances of int class.
If user has entered something other than an integer -- the program will tell the user.
Then it converts this list to a tuple and prits it.

```python
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
```

## 3

This task can be solved with list slicing.
Since `.readlines()` method returns a list, we can simply use 'slice step' to skip printing uneven lines:

```python
fname: str = input("Please enter filename: ")
if not path.exists(fname):
    print("File does not exist.")
    return 1
with open(fname, 'r') as file:
    content: List[str] = file.readlines()
    [print(l) for l in content[1::2]]
return 0
```

Here `content[1::2]` means 'skip first line'(uneven) and then 'print every second element'(wich will be even).


## 4

For this task I used an html parser (lxml is not standard though widespread).

```python
from lxml.html import parse

doc: str = input("Please enter document to parse: ")
try:
    doc = parse(doc).getroot()
except OSError as e:
    print(f"{e}\nDocument does not exist.")
    return 1
[print(t.text_content()) for t in doc.cssselect('title')]
return 0
```

Here, the main element is `.cssselect()` method, which simply searches for title tag.
In case there are more than one title tag, list comprehension will sort this out.

## 5

After consulting the emoji module documentation, I have decided that the simples way to do the task would be to use whitespace as a delimiter for input text and just apply `emojize()` method to see if any words can be turned in an emoji.
The downside of this method is that each word is considered separately, which means that emoji codes that have more than one word in them can't appear.

```python
from sys import argv
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
```

## 6

The text of this program is a bit too long. Could be shorter, but it is what it is.

In short, I used `psutil` module to get some basic system information, wrote a function to convert bytes to gigabytes and another one to visualize resource usage, added some string formatting and then [cobbled everything together](./task6.py).

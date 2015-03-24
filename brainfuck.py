#!/usr/bin/python
#
# Brainfuck Interpreter
# Copyright 2011 Sebastian Kaspari
#
# Usage: ./brainfuck.py [FILE]

import sys
import getch

def execute(filename):
  with open(filename, "r") as f:
      evaluate(f.read())


def evaluate(code):
  code     = cleanup(list(code))
  bracemap = buildbracemap(code)

  cells, codeptr, cur_ptr = [0], 0, 0

  while codeptr < len(code):
    command = code[codeptr]

    if command == ">":
      cur_ptr += 1
      if cur_ptr == len(cells): cells.append(0)

    if command == "<":
      cur_ptr = 0 if cur_ptr <= 0 else cur_ptr - 1

    if command == "+":
      cells[cur_ptr] = cells[cur_ptr] + 1 if cells[cur_ptr] < 255 else 0

    if command == "-":
      cells[cur_ptr] = cells[cur_ptr] - 1 if cells[cur_ptr] > 0 else 255

    if command == "[" and cells[cur_ptr] == 0: codeptr = bracemap[codeptr]
    if command == "]" and cells[cur_ptr] != 0: codeptr = bracemap[codeptr]
    if command == ".":
        sys.stdout.write(chr(cells[cur_ptr]))
    if command == ",": cells[cur_ptr] = ord(getch.getch())

    codeptr += 1


def cleanup(code):
  return filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code)


def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap


def main():
  if len(sys.argv) == 2: execute(sys.argv[1])
  else: print "Usage:", sys.argv[0], "filename"

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print "\n Recieved Interrupt Signal. Bye...."
        import sys
        sys.exit()

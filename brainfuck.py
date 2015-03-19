#!/usr/bin/python
#
# Brainfuck Interpreter
# Copyright 2011 Sebastian Kaspari
#
# Usage: ./brainfuck.py [FILE]

import sys
import getch
import code

def execute(filename):
  f = open(filename, "r")
  evaluate(f.read())
  f.close()


def evaluate(code):
  code, positions = cleanup(list(code))
  bracemap = buildbracemap(code)
  states = set()

  cells, codeptr, cellptr = [0], 0, 0
  steps = 0

  while codeptr < len(code):
    if codeptr > 0 and code[codeptr - 1] == "[":
      state_hash = get_state_hash(codeptr, cellptr, cells)
      if state_hash in states:
        line, column = positions[codeptr]
        print "%d:%d: Detected endless loop; %d steps." % (line, column, steps)
        return
      states.add(state_hash)

    command = code[codeptr]

    if command == ">":
      cellptr += 1
      if cellptr == len(cells): cells.append(0)

    if command == "<":
      cellptr = 0 if cellptr <= 0 else cellptr - 1

    if command == "+":
      cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

    if command == "-":
      cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

    if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
    if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
    if command == ".": sys.stdout.write(chr(cells[cellptr]))
    if command == ",": cells[cellptr] = ord(getch.getch())

    codeptr += 1
    steps += 1


def cleanup(code):
  clean_code = []
  positions = []
  line, column = 1, 1
  for c in code:
    if c == "\n":
      line += 1
      column = 1
    else:
      if c in ['.', ',', '[', ']', '<', '>', '+', '-']:
        clean_code.append(c)
        positions.append((line, column))
      column += 1
  return (clean_code, positions)
  

def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap


def get_state_hash(codeptr, cellptr, cells):
  hash = 1
  hash = hash * 17 + codeptr
  hash = hash * 31 + cellptr
  for i in cells:
    hash = hash * 13 + i
  return hash


def main():
  if len(sys.argv) == 2: execute(sys.argv[1])
  else: print "Usage:", sys.argv[0], "filename"

if __name__ == "__main__": main()


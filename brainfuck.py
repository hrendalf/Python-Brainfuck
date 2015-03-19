#!/usr/bin/python
#
# Brainfuck Interpreter
# Copyright 2011 Sebastian Kaspari
#
# Usage: ./brainfuck.py [FILE]

import sys
import getch

def execute(filename):
  f = open(filename, "r")
  evaluate(f.read())
  f.close()


def evaluate(code):
  code = cleanup(list(code))
  bracemap = buildbracemap(code)
  states = set()

  cells, codeptr, cellptr = [0], 0, 0
  steps = 0

  while codeptr < len(code):
    if codeptr > 0 and code[codeptr - 1] == "[":
      state_hash = get_state_hash(codeptr, cellptr, cells)
      # print "codeptr: %d; state; %d" % (codeptr, state_hash)
      if state_hash in states:
        print "Endless loop, codeptr=%d; after %d steps." % (codeptr, steps) 
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


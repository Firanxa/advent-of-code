# AoC 2024: A Brief History of Christmas

## Overview

These are my (ongoing) solutions to Advent of Code 2024, which include some end-of-the-day thoughts and comments on each puzzle.
I do everything in Python first, then translate to (or rethink in) Julia; the former to git 'er done, the latter to learn the language.

## Benchmarking

Since my goal is to complete the calendar as it goes, I'm not always prioritizing speed or the most optimal approach for my first solution.
Julia is generally much faster than Python, so I benchmark it against big inputs that you can download [here](https://bigboy.wiki/), with minimal changes from the Python solution unless otherwise noted.

Julia benchmarks are as follows:

### Day 1: Historian Hysteria

* **File size:** 29.92 MB
* **Input size:** 7M pairs
* **Part 1:** 10.402 ms (6 allocations: 61.04 MiB)
* **Part 2:** 330.003 ms (74 allocations: 299.69 MiB)

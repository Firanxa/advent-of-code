# AoC 2023

I measure my solutions' speed and memory usage using [BenchmarkTools](https://juliaci.github.io/BenchmarkTools.jl/stable/).
For reference, I also include the input file size and the number of lines, _N_, in the input.

- **Day 1:** _N_ = 1000 (21.3 KiB)
  - Part 1: 76.963 μs (3001 allocations: 134.34 KiB)
  - Part 2: 699.830 μs (35646 allocations: 2.10 MiB)
- **Day 2:** _N_ = 100 (10.4 KiB)
  - Part 1: 530.686 μs (11946 allocations: 730.73 KiB)
  - Part 2: 335.701 μs (7798 allocations: 495.11 KiB)
- **Day 3:** _N_ = 140 (19.3 KiB)
  - Part 1: 318.783 μs (5442 allocations: 361.52 KiB)
  - Part 2: 191.261 μs (4033 allocations: 617.80 KiB)
- **Day 4:** _N_ = 220 (25.1 KiB)
  - Part 1: 893.627 μs (10200 allocations: 1.26 MiB)
  - Part 2: 931.295 μs (10207 allocations: 1.26 MiB)
- **Day 5:** _N_ ~ 1e8 (5.6 KiB)
  - _Note:_ _N_ is the order of magnitude of the size of the search space in the naive approach.
  - Part 1: 56.195 μs (617 allocations: 84.53 KiB)
  - Part 2: 63.417 μs (709 allocations: 419.06 KiB)
- **Day 6:** _N_ ~ 1e7 (74 B)
  - _Note:_ _N_ is the order of magnitude of a number concatenated from an input list of numbers.
  - Part 1: 1.383 μs (10 allocations: 1.25 KiB)
  - Part 2: 338.755 ns (8 allocations: 768 bytes)
- **Day 7:** _N_ = 1000 (9.7 KiB)
  - Part 1: 545.252 μs (22007 allocations: 1.30 MiB)
  - Part 2: 606.978 μs (23343 allocations: 1.36 MiB)
- **Day 8:** _N_ = 788 (13.3 KiB)
  - Part 1: 589.493 μs (10263 allocations: 927.30 KiB)
  - Part 2: 2.421 ms (10265 allocations: 927.44 KiB)

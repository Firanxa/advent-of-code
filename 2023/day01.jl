using BenchmarkTools

# In the solution to Part 2, each number written out in English is replaced with a numeric
# string. The replacement contains the corresponding digit and the first and last letters
# of the word to account for possible overlaps between adjacent words. (For example,
# "eighthree" should be read as "eight three").
const _DIGITS_DICT = Dict{String, String}(
    "one" => "o1e",
    "two" => "t2o",
    "three" => "t3e",
    "four" => "f4r",
    "five" => "f5e",
    "six" => "s6x",
    "seven" => "s7n",
    "eight" => "e8t",
    "nine" => "n9e"
)

function _parse_line_to_int(line::String) :: Integer
    line = filter(isdigit, line)
    value = parse(Int, line[begin] * line[end])
    return value
end

function _parse_words_to_digits(line::String)
    for (word, num) in _DIGITS_DICT
        if occursin(word, line)
            line = replace(line, word => num)
        end
    end
    return line
end

function part1_day01(lines::Vector{String}) :: Integer
    lines = _parse_line_to_int.(lines)
    return sum(lines)
end

function part2_day01(lines::Vector{String}) :: Integer
    # Once digits have been inserted for the corresponding words, the problem setup is the
    # same as in Part 1.
    lines = _parse_words_to_digits.(lines)
    return part1_day01(lines)
end

if abspath(PROGRAM_FILE) == @__FILE__
    # Get puzzle input.
    lines = readlines("inputs/day01.txt")
    
    # Part 1.
    part1_ans = part1_day01(lines) # 54304
    println("2023 DAY 1 / PART 1")
    println("================================================")
    println("Answer:     $part1_ans")
    print("Benchmark:")
    @btime part1_day01(lines)
    
    println()

    # Part 2.
    part2_ans = part2_day01(lines) # 54418
    println("2023 DAY 1 / PART 2")
    println("================================================")
    println("Answer:     $part2_ans")
    print("Benchmark:")
    @btime part2_day01(lines)
end

using BenchmarkTools

function part1_day04(lines::Vector{String})
    total_points = 0
    for line in lines
        winning_nums, card_nums = _parse_line(line)
        matches = _matches(Set{Int}(winning_nums), Set{Int}(card_nums))
        total_points += _points(matches)
    end
    return total_points
end

function part2_day04(lines::Vector{String})
    card_counts = Dict{Int, Int}(i => 1 for i in eachindex(lines))
    for (i, line) in enumerate(lines)
        winning_nums, card_nums = _parse_line(line)
        matches = _matches(Set{Int}(winning_nums), Set{Int}(card_nums))
        # Add copies of the next cards for each (winning) copy of the currently held card.
        for k in 1:matches
            card_counts[i + k] += card_counts[i]
        end
    end
    return sum(values(card_counts))
end

function _matches(winning_nums::Set{Int}, card_nums::Set{Int})
    return length(intersect(winning_nums, card_nums))
end

function _points(matches::Int)
    return matches > 0 ? 2^(matches - 1) : 0
end

function _parse_line(line::String) :: Tuple{Vector{Int}, Vector{Int}}
    # Parse the line into the winning numbers and card numbers.
    numbers = split(line, ": ")[2]
    winning_nums, card_nums = split(numbers, "|")
    winning_nums = parse.(Int, split(winning_nums))
    card_nums = parse.(Int, split(card_nums))
    return winning_nums, card_nums
end

if abspath(PROGRAM_FILE) == @__FILE__
    # Get puzzle input.
    lines = readlines("inputs/day04.txt")
    
    # Part 1.
    part1_ans = part1_day04(lines) # 26346
    println("2023 DAY 4 / PART 1")
    println("================================================")
    println("Answer:     $part1_ans")
    print("Benchmark:")
    @btime part1_day04(lines)
    
    println()

    # Part 2.
    part2_ans = part2_day04(lines) # 8467762
    println("2023 DAY 4 / PART 2")
    println("================================================")
    println("Answer:     $part2_ans")
    print("Benchmark:")
    @btime part2_day04(lines)
end

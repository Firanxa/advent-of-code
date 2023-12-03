using BenchmarkTools

# A Record is the subset of cubes revealed in one play of the Game. A Game is uniquely
# identified by an ID and its Record(s). All of this is parsed from the puzzle input:
#   
#   Game 1: 10 green, 9 blue, 1 red; 1 red, 7 green; 11 green, 6 blue; 8 blue, 12 green
#   ...
#
struct Record
    red::Integer
    green::Integer
    blue::Integer
end

struct Game
    id::Integer
    records::Vector{Record}
end

function _parse_to_record(s::AbstractString) :: Record
    red, green, blue = 0, 0, 0
    cube_counts = split(s, ", ")
    for cube_count in cube_counts
        count = parse(Int, filter(isdigit, cube_count))
        cube_type = filter(isletter, cube_count)
        if startswith(cube_type, 'r')
            red = count
        elseif startswith(cube_type, 'g')
            green = count
        else
            blue = count
        end
    end
    return Record(red, green, blue)
end

function _parse_input(lines::Vector{String}) :: Vector{Game}
    games = Game[]
    for line in lines
        id_str, result_str = split(line, ": ")
        id = parse(Int, id_str[6:end])
        results = split(result_str, "; ")
        records = _parse_to_record.(results)
        push!(games, Game(id, records))
    end
    return games
end

function part1_day02(lines::Vector{String}; rgb_lims=(12, 13, 14)) :: Integer
    _is_valid_record(r::Record) = all((r.red, r.green, r.blue) .<= rgb_lims)
    games = _parse_input(lines)
    ids_sum = 0
    for game in games
        if all(_is_valid_record.(game.records))
            ids_sum += game.id
        end
    end
    return ids_sum
end

function part2_day02(lines::Vector{String}) :: Integer
    games = _parse_input(lines)
    power_sum = 0
    for game in games
        red_max, green_max, blue_max = 0, 0, 0
        for record in game.records
            red_max = max(record.red, red_max)
            green_max = max(record.green, green_max)
            blue_max = max(record.blue, blue_max)
        end
        power_sum += red_max * green_max * blue_max
    end
    return power_sum
end

if abspath(PROGRAM_FILE) == @__FILE__
    # Get puzzle input.
    lines = readlines("inputs/day02.txt")

    # Part 1.
    part1_ans = part1_day02(lines) # 2239
    println("2023 DAY 2 / PART 1")
    println("================================================")
    println("Answer:     $part1_ans")
    print("Benchmark:")
    @btime part1_day02(lines)
    
    println()

    # Part 2.
    part2_ans = part2_day02(lines) # 83435
    println("2023 DAY 2 / PART 2")
    println("================================================")
    println("Answer:     $part2_ans")
    print("Benchmark:")
    @btime part2_day02(lines)
end

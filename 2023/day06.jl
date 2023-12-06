using BenchmarkTools

function part1_day06(lines::Vector{String})
    times_str, records_str = lines
    times = parse.(Int, split(split(times_str, ":")[2]))
    records = parse.(Int, split(split(records_str, ":")[2]))
    solution = 1
    for (time, record) in zip(times, records)
        winning_ways = 0
        # Hold the button for t ms to get a speed of t m/s.
        for t in 1:time
            distance = (time - t) * t
            if distance > record
                winning_ways += 1
            end
        end
        solution *= winning_ways
    end
    return solution
end

function part2_day06(lines::Vector{String})
    times_str, records_str = lines
    time = parse(Int, filter(isdigit, split(times_str, ":")[2]))
    record = parse(Int, filter(isdigit, split(records_str, ":")[2]))
    
    # Using the fact that distance = (time - t) * t, the requirement that distance > record
    # is equivalent to the quadratic inequality 0 > t^2 - time * t + record. Solve for the
    # endpoints of the open interval (t1, t2) that satisfy the inequality. Since this
    # parabola opens upward, the floor of the difference t2 - t1 is the number of integer
    # values t in (t1, t2) that satisfy the inequality, i.e. that result in a speed that
    # will break the record. 
    t1 = div(time - sqrt(time^2 - 4 * record), 2)
    t2 = div(time + sqrt(time^2 - 4 * record), 2)
    return floor(Int, t2 - t1)
end

if abspath(PROGRAM_FILE) == @__FILE__
    # Get puzzle input.
    lines = readlines("inputs/day06.txt")

    # Part 1.
    part1_ans = part1_day06(lines) # 500346
    println("2023 DAY 6 / PART 1")
    println("================================================")
    println("Answer:     $part1_ans")
    print("Benchmark:")
    @btime part1_day06(lines)
    
    println()

    # Part 2.
    part2_ans = part2_day06(lines) # 42515755
    println("2023 DAY 6 / PART 2")
    println("================================================")
    println("Answer:     $part2_ans")
    print("Benchmark:")
    @btime part2_day06(lines)
end

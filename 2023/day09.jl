using BenchmarkTools

function part1_day09(lines::Vector{String})
    extrapolated_total = 0
    for line in lines
        seq = _parse_sequence(line)
        last_terms = _generate_terms(seq)
        extrapolated_terms = _extrapolate_terms(last_terms)
        extrapolated_total += extrapolated_terms[1]
    end
    return extrapolated_total
end

function part2_day09(lines::Vector{String})
    extrapolated_total = 0
    for line in lines
        seq = _parse_sequence(line)
        first_terms = _generate_terms(seq, first=true)
        extrapolated_terms = _extrapolate_terms(first_terms, first=true)
        extrapolated_total += extrapolated_terms[1]
    end
    return extrapolated_total
end

function _extrapolate_terms(history::Vector{Int}; first::Bool=false)
    m = length(history)
    extrapolated_terms = zeros(Int, m)
    for i in (m - 1):-1:1
        if first
            extrapolated_terms[i] = history[i] - extrapolated_terms[i + 1]
        else
            extrapolated_terms[i] = extrapolated_terms[i + 1] + history[i]
        end
    end
    return extrapolated_terms
end

function _generate_terms(seq::Vector{Int}; first::Bool=false)
    n = length(seq)
    start_index = 2
    terms = Vector{Int}()
    if first
        push!(terms, seq[1])
    else
        push!(terms, seq[n])
    end

    all_zeros = zeros(Int, n)
    while seq != all_zeros
        # Make a deep copy of the sequence so that the differences can be written in place.
        seq_copy = copy(seq)
        # Since the length of the sequence of differences decreases by 1 at each iteration,
        # it can be treated as a sequence of length n but padded with zeros.
        @views(seq[1:(start_index - 1)] .= 0)
        for i in start_index:n
            seq[i] = seq_copy[i] - seq_copy[i - 1]
        end
        if first
            push!(terms, seq[start_index])
        else
            push!(terms, seq[n])
        end
        start_index += 1
    end
    return terms
end

function _parse_sequence(line::String)
    return parse.(Int, split(line))
end

if abspath(PROGRAM_FILE) == @__FILE__
    lines = readlines("inputs/day09.txt")

    # Part 1.
    part1_ans = part1_day09(lines) # 1972648895
    println("2023 DAY 9 / PART 1")
    println("================================================")
    println("Answer:     $part1_ans")
    print("Benchmark:")
    @btime part1_day09(lines)
    
    println()

    # Part 2.
    part2_ans = part2_day09(lines) # 919
    println("2023 DAY 9 / PART 1")
    println("================================================")
    println("Answer:     $part2_ans")
    print("Benchmark:")
    @btime part2_day09(lines)    
end

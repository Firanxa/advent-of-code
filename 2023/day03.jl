using BenchmarkTools

function _parse_strings_to_matrix(vec::Vector{String}) :: Matrix{Char}
    # For more general use, this function could assert that the lengths of each string in
    # `vec` are equal to ensure the list of strings can be represented by a char matrix.
    # Credit goes to this topic on the Julia forums:
    #   https://discourse.julialang.org/t/converting-a-array-of-strings-to-an-array-of-char/35123/3
    @assert !isempty(vec)
    m, n = length(vec), length(vec[1])
    A = Matrix{Char}(undef, m, n)
    for i in eachindex(vec), (j, ch) in enumerate(vec[i])
        A[i, j] = ch
    end
    return A
end

function _neighbors(x, y, dims::Tuple{Int, Int}) :: Vector{Tuple{Int, Int}}
    m, n = dims
    neighbors_coords = Tuple{Int, Int}[]

    # Eight edge cases to consider:
    # 1. Top left corner
    if (x, y) == (1, 1)
        x_range = x:(x + 1)
        y_range = y:(y + 1)
    # 2. Top right corner
    elseif (x, y) == (1, n)
        x_range = x:(x + 1)
        y_range = (y - 1):y
    # 3. Top interior border
    elseif x == 1
        x_range = x:(x + 1)
        y_range = (y - 1):(y + 1)
    # 4. Bottom left corner
    elseif (x, y) == (m, 1)
        x_range = (x - 1):x
        y_range = y:(y + 1)
    # 5. Bottom right corner
    elseif (x, y) == (m, n)
        x_range = (x - 1):x
        y_range = (y - 1):y
    # 6. Bottom interior border
    elseif x == m
        x_range = (x - 1):x
        y_range = (y - 1):(y + 1)
    # 7. Left interior border
    elseif y == 1
        x_range = (x - 1):(x + 1)
        y_range = y:(y + 1)
    # 8. Right interior border
    elseif y == n
        x_range = (x - 1):(x + 1)
        y_range = (y - 1):y
    # Interior vertices
    else
        x_range = (x - 1):(x + 1)
        y_range = (y - 1):(y + 1)
    end
    for i in x_range, j in y_range
        # Exclude the point itself; it's not its own neighbor.
        if (i, j) != (x, y)
            push!(neighbors_coords, (i, j))
        end
    end
    return neighbors_coords
end

function part1_day03(lines::Vector{String}) :: Integer
    A = _parse_strings_to_matrix(lines)

    # Track which numbers are adjacent to a symbol.
    m, n = size(A)
    is_valid_at = falses(m, n)
    
    # Note that '$' has to be escaped in a Julia string. The backslash is not one of the
    # valid symbols.
    symbols = "!@#\$%^&*()_+-=/"
    
    # Mark which digits are part of a valid number because they neighbor a symbol.
    for i in 1:m, j in 1:n
        if A[i, j] in symbols
            for neighbor_coord in _neighbors(i, j, (m, n))
                is_valid_at[neighbor_coord...] = isnumeric(A[neighbor_coord...])
            end
        end
    end
    
    # Parse the valid digits into the whole part number. Also mark which digits have
    # already been parsed, so that there are no repeats!
    visited = falses(m, n)
    part_nums = Int[]
    for i in 1:m, j in 1:n
        if !visited[i, j] && is_valid_at[i, j]
            num_str = A[i, j]
            # Walk left.
            curr_y = j - 1
            while curr_y >= 1 && isnumeric(A[i, curr_y])
                num_str = A[i, curr_y] * num_str
                visited[i, curr_y] = true
                curr_y -= 1
            end
            # Walk right.
            curr_y = j + 1
            while curr_y <= n && isnumeric(A[i, curr_y])
                num_str *= A[i, curr_y]
                visited[i, curr_y] = true
                curr_y += 1
            end
            push!(part_nums, parse(Int, num_str))
        end
    end
    return sum(part_nums)
end

function part2_day03(lines::Vector{String}) :: Integer
    A = _parse_strings_to_matrix(lines)
    m, n = size(A)
    
    # This time, find the coordinates of every gear.
    gear_coords = Tuple{Int, Int}[]
    for i in 1:m, j in 1:n
        if A[i, j] == '*'
            push!(gear_coords, (i, j))
        end
    end
    
    # Identify the part numbers adjacent to every gear, in the same manner as in Part 1.
    # This time, enumerate the gears so as to track which numbers border each gear.
    is_valid_at = Matrix{NamedTuple{(:gear_id, :is_numeric), Tuple{Int, Bool}}}(undef, m, n)

    # is_numeric should be set to false for all (i, j), to account for any undefined
    # behavior from initialization.
    for i in eachindex(is_valid_at)
        is_valid_at[i] = (gear_id=-1, is_numeric=false)
    end
    
    for (id, coord) in enumerate(gear_coords)
        for neighbor_coord in _neighbors(coord..., (m, n))
            is_valid_at[neighbor_coord...] = (gear_id=id, is_numeric=isnumeric(A[neighbor_coord...]))
        end
    end
    
    visited = falses(m, n)
    gear_nums_dict = Dict{Int, Vector{Int}}()
    for i in 1:m, j in 1:n
        neighbor = is_valid_at[i, j]
        if !visited[i, j] && neighbor.is_numeric
            num_str = A[i, j]
            # Walk left.
            curr_y = j - 1
            while curr_y >= 1 && isnumeric(A[i, curr_y])
                num_str = A[i, curr_y] * num_str
                visited[i, curr_y] = true
                curr_y -= 1
            end
            # Walk right.
            curr_y = j + 1
            while curr_y <= n && isnumeric(A[i, curr_y])
                num_str *= A[i, curr_y]
                visited[i, curr_y] = true
                curr_y += 1
            end
            num = parse(Int, num_str)
            if haskey(gear_nums_dict, neighbor.gear_id)
                push!(gear_nums_dict[neighbor.gear_id], num)
            else
                gear_nums_dict[neighbor.gear_id] = [num]
            end
        end
    end
    
    gear_ratios_sum = 0
    for gear_nums in values(gear_nums_dict)
        if length(gear_nums) == 2
            gear_ratios_sum += prod(gear_nums)
        end
    end
    return gear_ratios_sum
end

if abspath(PROGRAM_FILE) == @__FILE__
    # Get puzzle input.
    lines = readlines("inputs/day03.txt")
    
    # Part 1.
    part1_ans = part1_day03(lines) # 537732
    println("2023 DAY 3 / PART 1")
    println("================================================")
    println("Answer:     $part1_ans")
    print("Benchmark:")
    @btime part1_day03(lines)
    
    println()

    # Part 2.
    part2_ans = part2_day03(lines) # 84883664
    println("2023 DAY 3 / PART 2")
    println("================================================")
    println("Answer:     $part2_ans")
    print("Benchmark:")
    @btime part2_day03(lines)
end

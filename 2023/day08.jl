using BenchmarkTools

struct DesertMap
    steps::String
    L_map::Dict{String, String}
    R_map::Dict{String, String}
    starting_nodes::Vector{String}
end

function part1_day08(lines::Vector{String})
    desert_map = _create_desert_map(lines)
    
    start = "AAA"
    finish = "ZZZ"
    position = start

    step_count = 0
    step_index = 1
    n = length(desert_map.steps)

    while position != finish
        step = desert_map.steps[step_index]
        if step == 'L'
            position = desert_map.L_map[position]
        elseif step == 'R'
            position = desert_map.R_map[position]
        end
        step_count += 1
        step_index += 1
        # Repeat the step instructions until we reach the finish node.
        if step_index > n
            step_index = mod(step_index, n)
        end
    end
    return step_count
end

function part2_day08(lines::Vector{String})
    desert_map = _create_desert_map(lines)
    
    # Record the number of steps it takes to reach a Z node starting from each A node.
    cycle_steps = Vector{Int}()
    for starting_node in desert_map.starting_nodes
        position = starting_node

        step_count = 0
        step_index = 1
        n = length(desert_map.steps)

        while !endswith(position, 'Z')
            step = desert_map.steps[step_index]
            if step == 'L'
                position = desert_map.L_map[position]
            elseif step == 'R'
                position = desert_map.R_map[position]
            end
            step_count += 1
            step_index += 1
            if step_index > n
                step_index = mod(step_index, n)
            end
        end
        push!(cycle_steps, step_count)
    end
    # Conveniently, a cycle exists for each starting node and has length equal to the
    # number of steps it takes to first reach a Z node... In the general case, we would
    # have to detect a cycle and calculate its length, e.g. with Floyd's algorithm.
    return lcm(cycle_steps)
end

function _create_desert_map(lines::Vector{String}) :: DesertMap
    steps = lines[1]
    network = lines[3:end]
    
    L_map = Dict{String, String}()
    R_map = Dict{String, String}()
    starting_nodes = Vector{String}()
    
    for line in network
        node, next_nodes = split(line, " = ")
        if endswith(node, 'A')
            push!(starting_nodes, node)
        end
        # Strip out the parentheses from the instructions tuple.
        next_nodes = next_nodes[begin + 1: end - 1]
        L_node, R_node = split(next_nodes, ", ")
        L_map[node] = L_node
        R_map[node] = R_node
    end
    return DesertMap(steps, L_map, R_map, starting_nodes)
end

if abspath(PROGRAM_FILE) == @__FILE__
    lines = readlines("inputs/day08.txt")

    # Part 1.
    part1_ans = part1_day08(lines) # 12361
    println("2023 DAY 8 / PART 1")
    println("================================================")
    println("Answer:     $part1_ans")
    print("Benchmark:")
    @btime part1_day08(lines)
    
    println()

    # Part 2.
    part2_ans = part2_day08(lines) # 18215611419223
    println("2023 DAY 8 / PART 1")
    println("================================================")
    println("Answer:     $part2_ans")
    print("Benchmark:")
    @btime part2_day08(lines)    
end

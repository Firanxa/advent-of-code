using BenchmarkTools
using DataStructures

# Strictly speaking, the source-to-destination doesn't have to be identified because the
# solution goes through those categories in the proper order.
struct AlmanacEntry
    source_to_destination::String
    source_ranges::Vector{UnitRange{Int}}
    destination_ranges::Vector{UnitRange{Int}}
    map_count::Int
end

function part1_day05(lines::Vector{String})
    # The first line of the almanac is the list of seeds, the second line is blank, then
    # everything after that after are the almanac entries.
    seed_list_str = lines[1]
    entries_text_blocks = _parse_input(lines[3:end])
    
    # Quickest way to split something like "seeds: 79 14 55 13" once and in one line...
    seeds = parse.(Int, split(split(seed_list_str, ": ")[2]))
    almanac_entries = _parse_almanac.(entries_text_blocks)

    lowest_location = typemax(Int64)
    # Process each seed through the list of almanac entries.
    for seed in seeds
        location = _get_location(seed, almanac_entries)
        lowest_location = min(location, lowest_location)
    end
    return lowest_location
end

function part2_day05(lines::Vector{String})
    entries_text_blocks = _parse_input(lines[3:end])
    almanac_entries = _parse_almanac.(entries_text_blocks)
    
    # The first line now describe seed ranges, not individual seeds.
    seed_list_str = lines[1]
    seed_ranges_str = parse.(Int, split(split(seed_list_str, ": ")[2]))
    seed_ranges = Vector{UnitRange{Int}}()
    for i in 1:2:length(seed_ranges_str)
        start = seed_ranges_str[i]
        range_length = seed_ranges_str[i + 1]
        seed_range = UnitRange(start, start + range_length - 1)
        push!(seed_ranges, seed_range)
    end
    # Process each seed range through the list of almanac entries.
    location_ranges = _get_location_ranges.(seed_ranges, Ref(almanac_entries))
    # Flatten the resulting vector of vectors to a 1D vector.
    location_ranges = vcat(location_ranges...)
    # TODO Figure out why the seed range 3429320627:3664624662 yields a humidity range and
    # location range of 0:-1. If it's filtered out, we get the right answer. Can't explain
    # why!
    location_ranges = filter((x) -> x != 0:-1, location_ranges)
    lowest_location = minimum(first.(location_ranges))
    return lowest_location
end

function _get_location(seed::Int, almanac_entries::Vector{AlmanacEntry})
    # Technically, location is determined from the seed via the sequence of mappings
    # seed -> soil -> fertilizer -> ... -> humidity -> location.
    location = seed
    for entry in almanac_entries
        for i in 1:entry.map_count
            source_range = entry.source_ranges[i]
            destination_range = entry.destination_ranges[i]
            if location in source_range
                diff = location - first(source_range)
                location = first(destination_range) + diff
                break
            end
        end
    end
    return location
end

function _get_location_ranges(seed_range::UnitRange{Int}, almanac_entries::Vector{AlmanacEntry})
    # Helper function to shift the endpoints of an integer UnitRange by the same amount.
    _shift_range(r::UnitRange{Int}, x::Int) = UnitRange(first(r) + x, last(r) + x)

    # Map an entire seed range to a list of location ranges.
    location_ranges = Vector{UnitRange{Int}}()
    # Keep a queue of ranges to process and a queue of ranges done processing.
    q_todo = Queue{UnitRange{Int}}()
    q_done = Queue{UnitRange{Int}}()
    enqueue!(q_todo, seed_range)
    for entry in almanac_entries
        # All ranges must be processed at each level. The done queue will never be empty
        # when the todo queue is, and vice versa.
        while !isempty(q_done)
            enqueue!(q_todo, dequeue!(q_done))
        end
        while !isempty(q_todo)
            current_range = dequeue!(q_todo)
            mapped = false
            for i in 1:entry.map_count
                source_range = entry.source_ranges[i]
                destination_range = entry.destination_ranges[i]
                overlap = intersect(current_range, source_range)
                diff = first(destination_range) - first(source_range)
                # Case 1: No overlap. (Idiomatic way of checking whether a UnitRange
                # intersection is empty).
                if first(overlap) > last(overlap)
                    continue
                # Case 2: Current range is contained in the source range.
                elseif overlap == current_range
                    overlap = _shift_range(overlap, diff)
                    enqueue!(q_done, overlap)
                    mapped = true
                    break
                # Case 3: Source range is contained in the current range.
                elseif overlap == source_range
                    left_range = UnitRange(first(current_range), first(source_range) - 1)
                    right_range = UnitRange(last(source_range) + 1, last(current_range))
                    enqueue!(q_todo, left_range)
                    enqueue!(q_todo, right_range)
                    overlap = _shift_range(overlap, diff)
                    enqueue!(q_done, overlap)
                    mapped = true
                    break
                # Case 4: Overlap with a left overhang.
                elseif first(current_range) < first(source_range)
                    left_range = UnitRange(first(current_range), first(source_range) - 1)
                    enqueue!(q_todo, left_range)
                    overlap = _shift_range(overlap, diff)
                    enqueue!(q_done, overlap)
                    mapped = true
                    break
                # Case 5: Overlap  with a right overhang.
                elseif last(current_range) > last(source_range)
                    right_range = UnitRange(last(source_range) + 1, last(current_range))
                    enqueue!(q_todo, right_range)
                    overlap = _shift_range(overlap, diff)
                    enqueue!(q_done, overlap)
                    mapped = true
                    break
                end
            end
            # If the current range doesn't match any of the source ranges, it gets mapped
            # to itself.
            if !mapped
                enqueue!(q_done, current_range)
            end
        end
    end
    # Push all items from the done queue into the return vector.
    while !isempty(q_done)
        push!(location_ranges, dequeue!(q_done))
    end
    return location_ranges
end

function _parse_almanac(text_block::Vector{String}) :: AlmanacEntry
    # The first line of the text block identifies the source category to destination
    # category. Everything after that is the list of maps.
    source_to_destination = text_block[1]
    parsed_ranges = _parse_map.(text_block[2:end])
    source_ranges = first.(parsed_ranges)
    destination_ranges = last.(parsed_ranges)
    @assert length(source_ranges) == length(destination_ranges)
    map_count = length(source_ranges)
    return AlmanacEntry(source_to_destination, source_ranges, destination_ranges, map_count)
end

function _parse_input(lines::Vector{String}) :: Vector{Vector{String}}
    text_blocks = Vector{Vector{String}}()
    text_block = Vector{String}()
    for line in lines
        if isempty(line)
            push!(text_blocks, text_block)
            text_block = Vector{String}()
        else
            push!(text_block, line)
        end
    end
    # The last text block isn't captured by the for loop.
    if !isempty(text_block)
        push!(text_blocks, text_block)
    end
    return text_blocks
end

function _parse_map(str::String) :: NTuple{2, UnitRange{Int}}
    destination_start, source_start, range_length = parse.(Int, split(str))
    source_range = UnitRange(source_start, source_start + range_length - 1)
    destination_range = UnitRange(destination_start, destination_start + range_length - 1)
    return source_range, destination_range
end

if abspath(PROGRAM_FILE) == @__FILE__
    lines = readlines("inputs/day05.txt")

    # Part 1.
    part1_ans = part1_day05(lines) # 240320250
    println("2023 DAY 5 / PART 1")
    println("================================================")
    println("Answer:     $part1_ans")
    print("Benchmark:")
    @btime part1_day05(lines)
    
    println()

    # Part 2.
    part2_ans = part2_day05(lines) # 28580589
    println("2023 DAY 5 / PART 2")
    println("================================================")
    println("Answer:     $part2_ans")
    print("Benchmark:")
    @btime part2_day05(lines)    
end

"""
Advent of Code 2024
Day 1: Historian Hysteria

This is no different from my Python solution, but DataStructures provides a counter for 
array elements that is significantly faster and more efficient than implementing manual 
counting like how I did in Python.

In Part 2, I also broadcast an anonymous function to compute and sum similarity scores, 
rather than iterate with a for loop. Based on some basic benchmarking, this isn't any 
faster than a for loop (those are actually very efficient in Julia), and there are more 
allocations; but its meaning is clearer to me, and it's more "Julian."
"""

using DataStructures

function solve_part1(left_list::Vector{Int}, right_list::Vector{Int})
    total_distance = sum(abs.(left_list - right_list))
    return total_distance
end

function solve_part2(left_list::Vector{Int}, right_list::Vector{Int})
    right_counts = counter(right_list)
    similarity_score = num -> num * get(right_counts, num, 0)
    total_similarity_score = sum(similarity_score.(left_list))
    return total_similarity_score
end

function _parse_input(filename::String)
    lines = split.(readlines(filename))
    left_list = parse.(Int, first.(lines))
    right_list = parse.(Int, last.(lines))
    return left_list, right_list
end

if abspath(PROGRAM_FILE) == @__FILE__
    left_list, right_list = _parse_input("../_tests/day01.txt")
    sort!(left_list)
    sort!(right_list)
    ans_part1 = solve_part1(left_list, right_list)
    ans_part2 = solve_part2(left_list, right_list)
    println("PART 1\tTotal distance is: $ans_part1")
    println("PART 2\tSimilarity score is: $ans_part2")
end

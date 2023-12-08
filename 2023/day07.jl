using BenchmarkTools

# Use lexicographic ordering to rank hands. Map the 10 and face cards, but keep J the same
# for Part 2.
const CARDS_DICT = Dict{Char, Char}(
    'T' => 'E',
    'J' => 'J',
    'Q' => 'X',
    'K' => 'Y',
    'A' => 'Z'
)

struct CamelCard
    hand::String
    bid::Int
    priority::Int
end

function part1_day07(lines::Vector{String})
    # Parse input to hands and bids.
    parsed_lines = _parse_line.(lines)
    hands = first.(parsed_lines)
    bids = last.(parsed_lines)

    # Rank all hands according to their strength.
    camel_cards = _create_card.(hands, bids)
    sort!(camel_cards, lt=isless)
    
    # Calculate total winnings.
    total_winnings = 0
    for (rank, camel_card) in enumerate(camel_cards)
        total_winnings += rank * camel_card.bid
    end
    return total_winnings    
end

function part2_day07(lines::Vector{String})
    # Same procedure as Part 1, but create modified CamelCards instead.
    parsed_lines = _parse_line.(lines)
    hands = first.(parsed_lines)
    bids = last.(parsed_lines)

    camel_cards = _create_modified_card.(hands, bids)
    sort!(camel_cards, lt=isless)

    total_winnings = 0
    for (rank, camel_card) in enumerate(camel_cards)
        total_winnings += rank * camel_card.bid
    end
    return total_winnings     
end

function _create_card(hand::AbstractString, bid::Int) :: CamelCard
    priority = _hand_priority(hand)
    return CamelCard(hand, bid, priority)
end

function _create_modified_card(hand::AbstractString, bid::Int) :: CamelCard
    # Jokers are now the lowest value card.
    joker = '1'
    # This replacement ensures that the Joker cannot be identified as the higher value
    # card when comparing hands of equal priority.
    modified_hand = replace(hand, 'J' => joker)
    modified_priority = _hand_priority(hand)
    return CamelCard(modified_hand, bid, modified_priority)
end

function _hand_priority(hand::AbstractString, joker::Char='1')
    card_counts = Dict{Char, Int}()
    for card in hand
        if haskey(card_counts, card)
            card_counts[card] += 1
        else
            card_counts[card] = 1
        end
    end
    # If creating a modified CamelCard: Create the strongest possible hand by replacing
    # each Joker with the card with the highest count, using value as a tiebreaker.
    if haskey(card_counts, joker)
        joker_count = card_counts[joker]
        # Edge case: Full house of Jokers.
        if joker_count != 5
            delete!(card_counts, joker)
            ___, highest_card = findmax(card_counts)
            card_counts[highest_card] += joker_count
        end
    end
    # The priority of hand types maps to an integer sequence according to the formula
    #
    #   priority = (# of most frequent card) - (# of unique cards)
    #
    max_count, ___ = findmax(card_counts)
    priority = max_count - length(card_counts)
    return priority
end

function _parse_line(line::String) :: Tuple{String, Int}
    hand, bid = split(line)
    parsed_hand = ""
    for card in hand
        if haskey(CARDS_DICT, card)
            parsed_hand *= CARDS_DICT[card]
        else
            parsed_hand *= card
        end
    end
    bid = parse(Int, bid)
    return parsed_hand, bid
end

function isless(a::CamelCard, b::CamelCard)
    # Compares and ranks hands according to hand type, or by strength of the hand in the
    # event of a tie.
    if a.priority == b.priority
        return a.hand < b.hand
    end
    return a.priority < b.priority
end

if abspath(PROGRAM_FILE) == @__FILE__
    lines = readlines("inputs/day07.txt")

    # Part 1.
    part1_ans = part1_day07(lines) # 249204891
    println("2023 DAY 7 / PART 1")
    println("================================================")
    println("Answer:     $part1_ans")
    print("Benchmark:")
    @btime part1_day07(lines)
    
    println()

    # Part 2.
    part2_ans = part2_day07(lines) # 249666369
    println("2023 DAY 7 / PART 2")
    println("================================================")
    println("Answer:     $part2_ans")
    print("Benchmark:")
    @btime part2_day07(lines)    
end

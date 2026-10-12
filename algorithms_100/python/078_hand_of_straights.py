"""
Hand of Straights - Start Every Group at the Smallest Card

Can the cards be split into groups of group_size consecutive values, every
card used exactly once? [1, 2, 3, 6, 2, 3, 4, 7, 8], group_size 3 -> True
(as [1, 2, 3], [2, 3, 4] and [6, 7, 8]).
"""


# --- algorithm ---
def can_form_straights(hand, group_size):
    """The smallest card left must start a group. O(n log n) for the sort."""
    if len(hand) % group_size != 0:
        return False
    count = {}
    for card in hand:
        count[card] = count.get(card, 0) + 1
    for card in sorted(count):          # distinct cards, smallest first
        starts = count[card]            # groups that must start at this card
        if starts > 0:
            for next_card in range(card, card + group_size):
                if count.get(next_card, 0) < starts:
                    return False        # a group would have a gap
                count[next_card] -= starts
    return True


# --- try it ---
print(can_form_straights([1, 2, 3, 6, 2, 3, 4, 7, 8], 3))   # -> True
print(can_form_straights([1, 2, 4, 5, 6, 7], 3))            # -> False
print(can_form_straights([1, 2, 3, 4, 5], 4))               # -> False
print(can_form_straights([2, 1, 3], 3))                     # -> True

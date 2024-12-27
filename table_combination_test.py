from cards.card import Card
from functions.combination_searchers.table_combination_searcher import Table_Combination_Searcher

# Royal flush
table = [Card('clubs', 'jack'), Card('clubs', '10'),
         Card('clubs', 'queen'), Card('clubs', 'ace'),
         Card('clubs', 'king')]

func = Table_Combination_Searcher(table)
print(f"Must be: Royal flush. Is: {func.execute()}")

# Straight flush
table = [Card('diamonds', '10'), Card('diamonds', '6'),
         Card('diamonds', '8'), Card('diamonds', '7'),
         Card('diamonds', '9')]

func = Table_Combination_Searcher(table)
print(f"Must be: Straight flush 40. Is: {func.execute()}")

# Four of a kind
table = [Card('diamonds', 'ace'), Card('clubs', 'ace'),
         Card('hearts', 'ace'), Card('spades', 'ace'),
         Card('spades', '8')]

func = Table_Combination_Searcher(table)
print(f"Must be: Four of a kind 56. Is: {func.execute()}")

# Full house
table = [Card('diamonds', '10'), Card('clubs', '10'),
         Card('hearts', '8'), Card('spades', '8'),
         Card('spades', '10')]

func = Table_Combination_Searcher(table)
print(f"Must be: Full house 46. Is: {func.execute()}")

# Flush
table = [Card('diamonds', '3'), Card('diamonds', '10'),
         Card('diamonds', 'queen'), Card('diamonds', '8'),
         Card('diamonds', '5')]

func = Table_Combination_Searcher(table)
print(f"Must be: Flush 38. Is: {func.execute()}")

# Straight
table = [Card('diamonds', '10'), Card('clubs', '7'),
         Card('hearts', '9'), Card('hearts', '8'),
         Card('spades', '6')]

func = Table_Combination_Searcher(table)
print(f"Must be: Straight 40. Is: {func.execute()}")

# Three of a kind
table = [Card('diamonds', '10'), Card('clubs', '10'),
         Card('hearts', 'queen'), Card('hearts', '8'),
         Card('spades', '10')]

func = Table_Combination_Searcher(table)
print(f"Must be: Three of a kind 30. Is: {func.execute()}")

# Two Pair
table = [Card('clubs', '8'), Card('clubs', '10'),
         Card('hearts', 'queen'), Card('hearts', '8'),
         Card('spades', '10')]

func = Table_Combination_Searcher(table)
print(f"Must be: Two Pair 36. Is: {func.execute()}")

# Pair
table = [Card('clubs', '2'), Card('clubs', '10'),
         Card('hearts', 'queen'), Card('hearts', '8'),
         Card('spades', 'queen')]

func = Table_Combination_Searcher(table)
print(f"Must be: Pair 24. Is: {func.execute()}")

# High card
table = [Card('clubs', 'ace'), Card('clubs', '10'),
         Card('hearts', 'queen'), Card('hearts', '8'),
         Card('spades', 'king')]

func = Table_Combination_Searcher(table)
print(f"Must be: 14 (ace). Is: {func.execute()}")
from cards.card import Card
from functions.combination_searchers.table_combination_searcher import Table_Combination_Searcher

# Royal flush
table = [Card('clubs', 'jack'), Card('clubs', '10'),
         Card('clubs', 'queen'), Card('clubs', 'ace'),
         Card('clubs', 'king')]

func = Table_Combination_Searcher(table)
print(f"Must be: Royal flush. Is: {func.execute()}")

# Flush
table = [Card('diamonds', '4'), Card('diamonds', '10'),
         Card('diamonds', 'queen'), Card('diamonds', '8'),
         Card('diamonds', '5')]

func = Table_Combination_Searcher(table)
print(f"Must be: Flush. Is: {func.execute()}")

# Straight
table = [Card('diamonds', '10'), Card('clubs', '7'),
         Card('hearts', '9'), Card('hearts', '8'),
         Card('spades', '6')]

func = Table_Combination_Searcher(table)
print(f"Must be: Straight. Is: {func.execute()}")

# Three of a kind
table = [Card('diamonds', '10'), Card('clubs', '10'),
         Card('hearts', 'queen'), Card('hearts', '8'),
         Card('spades', '10')]

func = Table_Combination_Searcher(table)
print(f"Must be: Three of a kind. Is: {func.execute()}")

# Two Pair
table = [Card('clubs', '8'), Card('clubs', '10'),
         Card('hearts', 'queen'), Card('hearts', '8'),
         Card('spades', '10')]

func = Table_Combination_Searcher(table)
print(f"Must be: Two Pair. Is: {func.execute()}")

# Pair
table = [Card('clubs', '2'), Card('clubs', '10'),
         Card('hearts', 'queen'), Card('hearts', '8'),
         Card('spades', '10')]

func = Table_Combination_Searcher(table)
print(f"Must be: Pair. Is: {func.execute()}")

# High card
table = [Card('clubs', 'ace'), Card('clubs', '10'),
         Card('hearts', 'queen'), Card('hearts', '8'),
         Card('spades', 'king')]

func = Table_Combination_Searcher(table)
print(f"Must be: 14 (ace). Is: {func.execute()}")
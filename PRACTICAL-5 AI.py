# Sonal Shukla CS23176

from itertools import permutations
def solve_cryptarithmetic():
    letters = "SENDMORY"  # Unique letters in puzzle
    digits = range(10)
    for perm in permutations(digits, len(letters)):
        s, e, n, d, m, o, r, y = perm
        # First letters cannot be zero
        if s == 0 or m == 0:
            continue
        # Form numbers
        send = 1000*s + 100*e + 10*n + d
        more = 1000*m + 100*o + 10*r + e
        money = 10000*m + 1000*o + 100*n + 10*e + y
        # Check condition
        if send + more == money:
            print("Solution Found!")
            print(f"S={s}, E={e}, N={n}, D={d}")
            print(f"M={m}, O={o}, R={r}, Y={y}")
            print(f"{send} + {more} = {money}")
            return
    print("No solution found.")
solve_cryptarithmetic()

# Sonal Shukla CS23176

n = int(input("Enter the size of the magic square: "))

magic_square = [[0 for _ in range(n)] for _ in range(n)]

num = 1
i = n // 2
j = n - 1

while num <= n * n:
    if i < 0 and j == n:
        i = 0
        j = n - 2
    else:
        if i < 0:
            i = n - 1
        if j == n:
            j = 0

    if magic_square[i][j] != 0:
        i = i + 1
        j = j - 2
        continue
    else:
        magic_square[i][j] = num
        num += 1

    i -= 1
    j += 1

# Print magic square
for i in range(n):
    for j in range(n):
        print(magic_square[i][j], end=" ")
    print()   
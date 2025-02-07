import random

N = 2

A = []
for i in range(N):
    row = []
    for j in range(N):
        row.append(random.randint(1, 5))
    A.append(row)

real_solution = [random.randint(1, 5) for i in range(N)]

B = [0, 0]
B[0] = A[0][0] * real_solution[0] + A[0][1] * real_solution[1]
B[1] = A[1][0] * real_solution[0] + A[1][1] * real_solution[1]


print(f"Matrix is {A}\nRight hand side is {B}")

solved = False
while not solved:
    x = []
    for i in range(N):
        x.append(int(input(f"Enter x{i}: ")))
    print(f"You proposed the solution {x}")

    test1 = A[0][0] * x[0] + A[0][1] * x[1]
    test2 = A[1][0] * x[0] + A[1][1] * x[1]

    if test1 == B[0] and test2 == B[1]:
        print("Correct!")
        solved = True
    else:
        print(
            "Incorrect, try again. First row error: ",
            test1 - B[0],
            "Second row error:",
            test2 - B[1],
        )

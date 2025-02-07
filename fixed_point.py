def g1(x: float) -> float:
    return x**2 - 2


def g2(x: float) -> float:
    return (x + 2) ** (1 / 2)


def g3(x: float) -> float:
    return 1 + (2 / x)


def g4(x: float) -> float:
    return -(1 / 3) * (x**2 - x - 2) + x


def find_fixedpoint(func, start, max_iter=10000, epsilon=1e-20):
    prev_x = start
    x_nx = None
    cnt = 0
    for _ in range(max_iter):
        x_nx = func(prev_x)

        print(x_nx)
        if abs(x_nx - prev_x) < epsilon:
            break

        prev_x = x_nx
        cnt += 1

    print(f"number of iteration {cnt}")
    print(f"Root is {x_nx}\n")


if __name__ == "__main__":
    find_fixedpoint(g1, 1)
    find_fixedpoint(g2, 1)
    find_fixedpoint(g3, 1)
    find_fixedpoint(g4, 1)

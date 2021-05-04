def generate(n):
    a, b, counter = 0, 1, 0

    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1

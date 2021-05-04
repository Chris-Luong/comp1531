def reduce(f, xs):
    # TODO: your code here
    if not xs:
        return None
    if len(xs) == 1:
        return xs[0]
    return f(reduce(f, xs[1:]), xs[0])


if __name__ == '__main__':
    print(reduce(lambda x, y: x + y, [1,2,3,4,5])) # pragma: no cover
    print(reduce(lambda x, y: x * y, [1,2,3,4,5]))
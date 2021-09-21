def best_fit(X, Y):
    xbar = sum(X) / len(X)
    ybar = sum(Y) / len(Y)
    n = len(X)  # or len(Y)

    numer = sum([xi * yi for xi, yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi ** 2 for xi in X]) - n * xbar ** 2

    m = numer / denum
    b = ybar - m * xbar

    print('best fit line:\ny = {:.2f} + {:.2f}x'.format(b, m))

    return m, b

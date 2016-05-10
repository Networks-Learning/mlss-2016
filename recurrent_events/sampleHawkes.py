import numpy as np

def sampleHawkes(lambda_0, alpha_0, w, T, Nev, seed=None):
    """Generates a sample of a Hawkes process until one of the following happens:
      - The next generated event is after T
      - Nev events have been generated.

    Returns: a tuple with the event times and the last generated time.
    """

    np.random.seed(seed)

    # First event is generated just as for a normal poisson process.

    tev = np.zeros(Nev)
    n = 0
    lambda_star = lambda_0
    next_arrival_time = np.random.exponential(scale=1.0 / lambda_star)
    tev[n] = next_arrival_time

    # Generate the next events
    n += 1
    while n < Nev:
        lambda_star = lambda_star + alpha_0
        next_arrival_time += np.random.exponential(scale=1.0 / lambda_star)

        if next_arrival_time < T:
            d = np.random.rand()
            lambda_s = lambda_0 + alpha_0 * np.sum(np.exp(-w * (next_arrival_time - tev[0:n - 1])))

            if d <= lambda_s / lambda_star:
                tev[n] = next_arrival_time
                lambda_star = lambda_s
                n += 1
        else:
            break

        # TODO: Should be increased here, or only in the 'then' branch above?
        # n += 1

    # TODO: Verify that this is correct.
    tev = tev[0:n - 1]

    if n == Nev:
        Tend = tev[-1]
    else:
        Tend = T

    return tev, Tend


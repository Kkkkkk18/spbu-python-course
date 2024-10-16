def prime_num(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def prime_generator():
    num = 2
    while True:
        if prime_num(num):
            yield num
        num += 1


def kth_prime_generator(k):

    prime_gen = prime_generator()
    prime = 0
    for _ in range(k):
        prime = next(prime_gen)
    return prime


s

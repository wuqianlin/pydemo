import concurrent.futures
import math
import time

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def generator():
    yield 112272535095293
    yield 112582705942171
    yield 112272535095293
    time.sleep(2)
    yield 115280095190773
    yield 115797848077099
    yield 1099726899285419


def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for prime in executor.map(is_prime, generator(), chunksize=10):
            print(f'%d is prime: {prime}')

if __name__ == '__main__':
    main()
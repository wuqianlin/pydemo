# This code calculates the fibonacci of some number many times and
# each time prints the total time it took to calculate the value
# @author Rodrigo Ramirez
import time
import timeit
import profile
import numba


# Calculates the Fibonacci of n
@numba.jit
def f(n):
    if n <= 2:
        return 1
    n1 = 1
    n2 = 1
    result = 0

    for i in range(3, n + 1):
        result = n1 + n2
        n2 = n1
        n1 = result

    print(result)
    return result


# Prints the average time it takes to calculate f(n)
def track_execution_speed():
    print("Average time to execute f(90) in nanoseconds\n")
    for i in range(200):
        start_time = time.time()
        for j in range(50):
            s = f(90)
            print(s)
        total_time = time.time() - start_time
        print(1e+9 * total_time/50)


cost = timeit.timeit('track_execution_speed()', 'from __main__ import track_execution_speed', number=1000)
profile.run('track_execution_speed()')
print(cost)
track_execution_speed()

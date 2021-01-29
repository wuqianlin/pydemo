import dis


def add(x, y):
    z = x + y
    return z


_x = " ".join(f"{b:02X}" for b in add.__code__.co_code)
print(_x)
print(add.__code__.co_code)
dis.dis(add)

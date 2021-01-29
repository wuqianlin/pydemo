"""
在try...except...finally语法中，如果有finally有return语句，
就算except语句块中有异常也不会抛出。
"""
# todo: Why


def final_return():
    try:
        int("invalid")
    except Exception as e:
        print("in except block")
        raise e
    finally:
        return


result = final_return()
print(result)

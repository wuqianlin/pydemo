import psutil


def killProcessByID(parent_pid: int):
    """
    If the parent process is not a "process group" but you want to kill it with the children,
    you can use psutil (https://pythonhosted.org/psutil/#processes).
    os.killpg cannot identify pid of a non-process-group.
    solution from: https://stackoverflow.com/questions/6549669/how-to-kill-process-and-child-processes-from-python
    """
    parent = psutil.Process(parent_pid)
    for child in parent.children(recursive=True):  # or parent.children() for recursive=False
        child.kill()
    parent.kill()

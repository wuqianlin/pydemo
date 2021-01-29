import warnings

warnings.simplefilter("always")


def fxn():
    warnings.warn("this is a warning", Warning)


with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    warnings.WarningMessage
    fxn()
    print(w[0])

with warnings.catch_warnings():
    warnings.warn("this is a warning2", Warning)

warnings.warn("this is a warning3", Warning)


def fxn2():
    warnings.warn("deprecated", DeprecationWarning)


with warnings.catch_warnings(record=True) as w:
    # Cause all warnings to always be triggered.
    warnings.simplefilter("always")
    # Trigger a warning.
    fxn2()
    # Verify some things
    assert len(w) == 1
    assert issubclass(w[-1].category, DeprecationWarning)
    assert "deprecated" in str(w[-1].message)

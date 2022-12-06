import sys
from os import path
sys.path.append(path.dirname('.'))

import classes

def test_unique():
    a = classes.Entity()
    b = classes.Entity()
    assert a != b, "Should be uniquely identified"

def test_copy():
    a = classes.Entity()
    b = classes.Entity(a.id.hex)
    assert a == b, "Should be equal"

if __name__ == "__main__":
    test_unique()
    test_copy()
    print("QC Pass")
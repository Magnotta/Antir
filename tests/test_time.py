import sys
from os import path
sys.path.append(path.dirname('.'))

from ..classes.time import Time

def test_repr():
    a = Time((13,20,33))
    assert repr(a) == "13, 20:33", f"Expected 13, 20:33 but got {repr(a)}"


def test_equal():
    a = (b := Time((1,1,1)))
    assert a == b, f"Expected True but got {a==b}"

def test_add_time():
    a = Time((13,12,16))
    b = Time((1,2,3))
    assert a + b == Time((14,14,19)), f"Expected (14, 14:19) but got ({a+b})"

def test_add_tuple():
    a = Time((13,12,16))
    b = (1,0,0)
    assert a + b == Time((14,12,16)), f"Expected (14, 12:16) but got ({a+b})"

def test_roundover():
    a = Time((0,6,9))
    b = Time((0,21874,65536))
    assert a + b == Time((957,4,25)), f"Expected (957, 22:16) but got ({a+b})"

if __name__ == "__main__":
    test_repr()
    test_equal()
    test_add_time()
    test_add_tuple()
    test_roundover()
    print("QC Pass")
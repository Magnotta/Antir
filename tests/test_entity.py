import sys
from os import path

SCRIPT_DIR = path.dirname(path.abspath(__file__))
sys.path.append(path.dirname(SCRIPT_DIR))

from classes.entity import Entity

def test_unique():
    a = Entity()
    b = Entity()
    assert a != b, "Should be uniquely identified"

    c = Entity()
    d = Entity()
    assert c != d, "Should be uniquely identified"

def test_copy():
    a = Entity()
    try:
        b = Entity(a.id)
    except ValueError:
        pass
    else:
        raise AssertionError('Copying should not be allowed')

def test_str():
    a = Entity(16)
    assert str(a) == (c:='10'), f'Should be equal but are {str(a)} and {c}'
    b = Entity(256)
    assert str(b) == (c:='100'), f'Should be equal but are {str(b)} and {c}'

if __name__ == "__main__":
    test_unique()
    test_copy()
    test_str()
    print("QC Pass")
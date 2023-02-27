import sys
from os import path

SCRIPT_DIR = path.dirname(path.abspath(__file__))
sys.path.append(path.dirname(SCRIPT_DIR))

from classes.entity import Entity

def test_unique():
    a = Entity()
    b = Entity()
    assert a != b, "Should be uniquely identified"

def test_copy():
    a = Entity()
    b = Entity(a.id.hex)
    assert a == b, "Should be equal"

if __name__ == "__main__":
    test_unique()
    test_copy()
    print("QC Pass")
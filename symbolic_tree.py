"""Data structures for symbolic values
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any
from z3 import Bool, And as z3_and, Or as z3_or, Not as z3_not, BoolRef

@dataclass(slots=True, frozen=True)
class Constraint:
    val: BoolRef
    birthday: int

def _and(x, y):
    if type(x) is bool and type(y) is bool:
        return x and y
    else:
        return z3_and(x, y)

def _or(x, y):
    if type(x) is bool and type(y) is bool:
        return x or y
    else:
        return z3_or(x, y)

def _not(x):
    if type(x) is bool:
        return not x
    else:
        return z3_not(x)

@dataclass(slots=True)
class Leaf():
    val: Any

    def merge(self, other: SymbolicTree) -> SymbolicTree:
        match self, other:
            case Leaf(v1), Leaf(v2):
                return Leaf((v1, v2))
            case _, Node(cond, left, right):
                return Node(cond, self.merge(left), self.merge(right))

    def map(self, f):
        return Leaf(f(self.val))

    def map2(self, f):
        return Leaf(f(self.val[0], self.val[1]))

    def bind(self, f):
        return f(self.val)

    def flatten(self):
        return self.val

    def __add__(self, other):
        return merge(self, other).map2(lambda x, y: x + y)
    
    def __sub__(self, other):
        return merge(self, other).map2(lambda x, y: x - y)

    def __mul__(self, other):
        return merge(self, other).map2(lambda x, y: x * y)

    def __truediv__(self, other):
        return merge(self, other).map2(lambda x, y: x // y)

    def __lt__(self, other):
        return merge(self, other).map2(lambda x, y: x < y)
    
    def __le__(self, other):
        return merge(self, other).map2(lambda x, y: x <= y)

    def __eq__(self, other):
        return merge(self, other).map2(lambda x, y: x == y)

    def __gt__(self, other):
        return merge(self, other).map2(lambda x, y: x > y)

    def __ge__(self, other):
        return merge(self, other).map2(lambda x, y: x >= y)


@dataclass(slots=True)
class Node:
    cond: Constraint
    left: SymbolicTree
    right: SymbolicTree

    def merge(self, other: SymbolicTree) -> SymbolicTree:
        match self, other:
            case Node(cond, left, right), Leaf(_):
                return Node(cond, left.merge(other), right.merge(other))
            case Node(cond1, left1, right1), Node(cond2, left2, right2):
                if cond1.birthday < cond2.birthday:
                    return Node(cond1, left1.merge(other), right1.merge(other))
                elif cond1.birthday == cond2.birthday:
                    assert cond1 == cond2
                    return Node(cond1, left1.merge(left2), right1.merge(right2))
                else:
                    return Node(cond2, self.merge(left2), self.merge(right2))

    def map(self, f):
        return Node(self.cond, self.left.map(f), self.right.map(f))

    def map2(self, f):
        return Node(self.cond, self.left.map2(f), self.right.map2(f))

    def bind(self, f):
        return Node(self.cond, self.left.bind(f), self.right.bind(f))

    def flatten(self):
        return _or(_and(self.cond.val, self.left.flatten()), _and(_not(self.cond.val), self.right.flatten()))

    def __add__(self, other):
        return merge(self, other).map2(lambda x, y: x + y)
    
    def __sub__(self, other):
        return merge(self, other).map2(lambda x, y: x - y)

    def __mul__(self, other):
        return merge(self, other).map2(lambda x, y: x * y)

    def __truediv__(self, other):
        return merge(self, other).map2(lambda x, y: x // y)

    def __lt__(self, other):
        return merge(self, other).map2(lambda x, y: x < y)
    
    def __le__(self, other):
        return merge(self, other).map2(lambda x, y: x <= y)

    def __eq__(self, other):
        return merge(self, other).map2(lambda x, y: x == y)

    def __gt__(self, other):
        return merge(self, other).map2(lambda x, y: x > y)

    def __ge__(self, other):
        return merge(self, other).map2(lambda x, y: x >= y)


SymbolicTree = Leaf | Node


def merge(t1: SymbolicTree, t2: SymbolicTree) -> SymbolicTree:
    return t1.merge(t2)

def fmap2(f, t1, t2):
    return merge(t1, t2).map2(f)

def liftA2(f):
    return lambda x, y: x.merge(y).map2(f)

def merge_blow(cond, t1: SymbolicTree, t2: SymbolicTree) -> SymbolicTree:
    match t1, t2:
        case Leaf(_), Leaf(_):
            return Node(cond, t1, t2)
        case Leaf(_), Node(cond2, left2, right2):
            if cond2.birthday > cond.birthday:
                return Node(cond, t1, t2)
            else:
                assert cond2.birthday < cond.birthday
                return Node(cond2, merge_blow(cond, t1, left2), merge_blow(cond, t1, right2))
        case Node(cond1, left1, right1), Leaf(_):
            if cond1.birthday > cond.birthday:
                return Node(cond, t1, t2)
            else:
                assert cond1.birthday < cond.birthday
                return Node(cond1, merge_blow(cond, left1, t2), merge_blow(cond, right1, t2))
        case Node(cond1, left1, right1), Node(cond2, left2, right2):
            if cond1.birthday > cond.birthday and cond2.birthday > cond.birthday:
                return Node(cond, t1, t2)
            else:
                if cond1.birthday < cond2.birthday:
                    return Node(cond1, merge_blow(cond, left1, t2), merge_blow(cond, right1, t2))
                elif cond1.birthday == cond2.birthday:
                    return Node(cond1, merge_blow(cond, left1, right1), merge_blow(cond, right1, right2))
                else:
                    return Node(cond2, merge_blow(cond, t1, left2), merge_blow(cond, t1, right2))


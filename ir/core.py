"""The core language
"""
from __future__ import annotations
from typing import Dict, Set
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Reg:
    reg: str

### Types
@dataclass(slots=True, frozen=True)
class Int: ...

@dataclass(slots=True, frozen=True)
class Bool: ...

Type = Int | Bool

### Instructions
@dataclass(slots=True, frozen=True)
class Load:
    dst: Reg
    const: int

@dataclass(slots=True, frozen=True)
class Fresh:
    dst: Reg
    ty: Type

@dataclass(slots=True)
class Assign:
    dst: Reg
    src: Reg

# Arithmetic operators
@dataclass(slots=True)
class Add:
    dst: Reg
    op1: Reg
    op2: Reg

@dataclass(slots=True)
class Sub:
    dst: Reg
    op1: Reg
    op2: Reg

@dataclass(slots=True)
class Mul:
    dst: Reg
    op1: Reg
    op2: Reg

@dataclass(slots=True)
class Div:
    dst: Reg
    op1: Reg
    op2: Reg

@dataclass(slots=True)
class Lt:
    dst: Reg
    op1: Reg
    op2: Reg

@dataclass(slots=True)
class Le:
    dst: Reg
    op1: Reg
    op2: Reg

@dataclass(slots=True)
class Eq:
    dst: Reg
    op1: Reg
    op2: Reg

@dataclass(slots=True)
class Gt:
    dst: Reg
    op1: Reg
    op2: Reg

@dataclass(slots=True)
class Ge:
    dst: Reg
    op1: Reg
    op2: Reg

# Logical operators
@dataclass(slots=True)
class And:
    dst: Reg
    op1: Reg
    op2: Reg

@dataclass(slots=True)
class Or:
    dst: Reg
    op1: Reg
    op2: Reg

@dataclass(slots=True)
class Not:
    dst: Reg
    op: Reg

### Control flows
@dataclass(slots=True)
class If:
    cond: Reg
    true_block: Block
    false_block: Block

### Debugging
@dataclass(slots=True)
class Debug:
    reg: Reg

Instr = Load | Assign | Add | Sub | Mul | Div\
      | Lt | Le | Eq | Ge | Gt\
      | And | Or | Not\
      | If\
      | Debug

### Block
@dataclass(slots=True)
class Block:
    instrs: list[Instr]
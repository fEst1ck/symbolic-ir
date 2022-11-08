"""The intermediate language
"""

from __future__ import annotations
from typing import Dict, Set
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Int: ...

@dataclass(slots=True, frozen=True)
class Bool: ...

Type = Int | Bool

@dataclass(slots=True, frozen=True)
class Reg:
    reg: str

@dataclass(slots=True, frozen=True)
class Label:
    label: str

# Instruction types
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

@dataclass(slots=True)
class Ge:
    dst: Reg
    op1: Reg
    op2: Reg


@dataclass(slots=True)
class If:
    cond: Reg
    true_block: Block
    false_block: Block

@dataclass(slots=True)
class While:
    cond: Reg
    block: Block

@dataclass(slots=True)
class Debug:
    reg: Reg


Instr = Load | Assign | Add | Sub | Mul | Div\
      | Lt | Le | Eq | Ge | Gt\
      | And | Or | Not\
      | If | While\
      | Debug

@dataclass(slots=True)
class Block:
    instrs: list[Instr]

    def mut_vars(self):
        def mut_vars_instr(instr: Instr) -> set[Reg]:
            match instr:
                case Load(dst, _):
                    return {dst}
                case Assign(dst, _):
                    return {dst}
                case Add(dst, _, _):
                    return {dst}
                case Sub(dst, _, _):
                    return {dst}
                case Mul(dst, _, _):
                    return {dst}
                case Div(dst, _, _):
                    return {dst}
                case Lt(dst, _, _):
                    return {dst}
                case Le(dst, _, _):
                    return {dst}
                case Eq(dst, _, _):
                    return {dst}
                case Ge(dst, _, _):
                    return {dst}
                case Gt(dst, _, _):
                    return {dst}
                case And(dst, _, _):
                    return {dst}
                case Or(dst, _, _):
                    return {dst}
                case Not(dst, _):
                    return {dst}
                case If(_, b1, b2):
                    return b1.mut_vars().union(b2.mut_vars())
                case While(_, b):
                    return b.mut_vars()
                case Debug(_):
                    return set()
        res = set()
        for instr in self.instrs:
            mut_vars = mut_vars_instr(instr)
            for reg in mut_vars: res.add(reg)
        return res

    def __iter__(self):
        return self.instrs.__iter__()
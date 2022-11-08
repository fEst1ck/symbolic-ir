"""IR interpreter
"""
from typing import Optional, Dict
from ir import Reg, Label, Instr,\
    Load, Fresh, Assign,\
    Add, Sub, Mul, Div,\
    Lt, Le, Eq, Ge, Gt,\
    And, Or, Not,\
    If, While,\
    Debug,\
    Block


Value = int | bool


def interp_instr(env: Dict[Reg, Value], instr: Instr):
    match instr:
        case Load(dst, const):
            env[dst] = const
        case Fresh(_):
            raise NotImplementedError
        case Assign(dst, src):
            env[dst] = env[src]
        case Add(dst, op1, op2):
            env[dst] = env[op1] + env[op2]
        case Sub(dst, op1, op2):
            env[dst] = env[op1] - env[op2]
        case Mul(dst, op1, op2):
            env[dst] = env[op1] * env[op2]
        case Div(dst, op1, op2):
            env[dst] = env[op1] // env[op2]
        case Lt(dst, op1, op2):
            env[dst] = env[op1] < env[op2]
        case Le(dst, op1, op2):
            env[dst] = env[op1] <= env[op2]
        case Eq(dst, op1, op2):
            env[dst] = env[op1] == env[op2]
        case Ge(dst, op1, op2):
            env[dst] = env[op1] >= env[op2]
        case Gt(dst, op1, op2):
            env[dst] = env[op1] > env[op2]
        case And(dst, op1, op2):
            env[dst] = env[op1] and env[op2] # env[op1] != 0 and env[op2] != 0
        case Or(dst, op1, op2):
            env[dst] = env[op1] or env[op2]
        case Not(dst, op):
            env[dst] = not env[op]
        case If(cond, b1, b2):
            if env[cond]:
                interp_block(env, b1)
            else:
                interp_block(env, b2)
        case While(cond, b):
            if env[cond]:
                interp_block(env, b)
                interp_instr(env, instr)
        case Debug(reg):
            print(f"debug: {reg.reg} = {env[reg]}")
        case _:
            raise NotImplementedError

def interp_block(env: Dict[Reg, Value], block: Block) -> Optional[Label]:
    for instr in block:
        interp_instr(env, instr)


if __name__ == '__main__':
    from text_format import parser
    import sys
    with open(sys.argv[1]) as f:
        block = parser.parse(f.read())
        init_env = dict()
        interp_block(init_env, block)
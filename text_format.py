"""Text format of the IR
"""
from ir import Reg, Label, Instr, Block,\
    Int, Bool,\
    Load, Fresh, Assign,\
    Add, Sub, Mul, Div,\
    Lt, Le, Eq, Ge, Gt,\
    And, Or, Not,\
    If, While,\
    Debug
from lark import Lark, Transformer, v_args


grammer = """
    ?block: "{" instr* "}"

    ?instr: load | fresh | assign
          | add | sub | mul | div
          | lt | le | eq | ge | gt
          | land | lor | lnot
          | debug
          | ifs | whiles

    load: reg "=" const ";"
    fresh: "fresh" reg ":" type ";"
    assign: reg "=" reg ";"
    add: reg "=" reg "+" reg ";"
    sub: reg "=" reg "-" reg ";"
    mul: reg "=" reg "*" reg ";"
    div: reg "=" reg "/" reg ";"
    lt: reg "=" reg "<" reg ";"
    le: reg "=" reg "<=" reg ";"
    eq: reg "=" reg "==" reg ";"
    ge: reg "=" reg ">=" reg ";"
    gt: reg "=" reg ">" reg ";"
    land: reg "=" reg "&&" reg ";"
    lor: reg "=" reg "||" reg ";"
    lnot: reg "=" "!" reg ";"
    ifs: "if" "(" reg ")" block ["else" block]
    whiles: "while" "(" reg ")" block
    debug: "debug" reg ";"

    ?type: "int"  -> ty_int
         | "bool" -> ty_bool

    reg: NAME

    label: "." NAME

    const: INT*

    COMMENT: /#.*/
    %import common (INT, WS)
    %import common.CNAME -> NAME
    %ignore COMMENT
    %ignore WS
"""


@v_args(inline=True)
class IRTransformer(Transformer):
    def block(self, *args):
        return Block(list(args))
    
    load = Load
    fresh = Fresh
    assign = Assign
    add = Add
    sub = Sub
    mul = Mul
    div = Div
    lt = Lt
    le = Le
    eq = Eq
    ge = Ge
    gt = Gt
    land = And
    lor = Or
    lnot = Not
    debug = Debug

    def ifs(self, reg, b1, b2):
        if type(b1) is not Block:
            b1 = Block([b1]) # wtf?
        if b2 is None:
            b2 = Block([])
        if type(b2) is not Block: # wtf?
            b2 = Block([b2])
        return If(reg, b1, b2)

    def whiles(self, reg, b):
        return While(reg, b)

    def ty_int(self):
        return Int()

    def ty_bool(self):
        return Bool()

    def reg(self, tok):
        return Reg(tok.value)

    def label(self, tok):
        return Label(tok.value)

    def const(self, digits):
        return int(''.join(digits))

    def INT(self, tok) -> int:
        return tok.value


parser = Lark(grammer, start='block')
parse = lambda text: IRTransformer().transform(parser.parse(text))
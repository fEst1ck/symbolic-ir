# Overview

This repo implements a symbolic executor for a simple intermediate language.

# Example

```
$ cat example/fac
{
    fresh x: int;
    fuel = 3;
    res = 1;
    zero = 0;
    one = 1;
    x_pos = x > zero;
    fuel_pos = fuel > zero;
    cond = fuel_pos && x_pos;
    while (cond) {
        res = res * x;
        x = x - one;
        fuel = fuel - one;
        x_pos = x > zero;
        fuel_pos = fuel > zero;
        cond = fuel_pos && x_pos;
    }
    debug res;
}
$ python se.py example/fac
debug: res = Node(cond=Constraint(val=And(True, x > 0)),
                left=Node(cond=Constraint(val=And(True, x - 1 > 0)),
                    left=Node(cond=Constraint(val=And(True, x - 1 - 1 > 0)),
                        left=Leaf(val=1*x*(x - 1)*(x - 1 - 1)),
                        right=Leaf(val=1*x*(x - 1))),
                    right=Leaf(val=1*x)),
                right=Leaf(val=1))
```

# Project structure

```
.
├── ir.py                  # IR
├── se.py                  # Symbolic executor
├── interp.py              # Interpreter
├── symbolic_tree.py       # Data structures
└── text_format.py         # Text format and parser
├── example                # Example programs           
```
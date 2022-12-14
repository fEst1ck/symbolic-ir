# Core language

```
# type
t := int | bool
# constant
c := n | b
# instruction
instr := x [: t] = c
       | fresh x : t
       | x [: t] = op x ...
       | if (x) block [else block]
# block
block := { instr* }
```

# Extended with tuple
```
t := ... | (t, ...)
instr := ...
       | x = (x, ...)
       | x = x.k
```
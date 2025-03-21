from z3 import *

solver = Solver()
x1, x2, x3 = Ints('x1 x2 x3')
solver.add(x1 > 0, x2 > 0, x3 > 0)

if solver.check() == sat:
    model = solver.model()
    solution = [model[x1], model[x2], model[x3]]
    print("Solution found:", solution)
else:
    print("No solution exists.")

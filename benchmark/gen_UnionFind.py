import re
import random
import time

var_declar = set()
result_logic = []
result_SPG = []

start_time = time.time()

for i in range(300):
    var_declar.add(f"x{i}")

for j in range(6):
    for num in range(5000*(j+1)):
        x1 = random.choice(list(var_declar))
        x2 = random.choice(list(var_declar))
        result_logic.append(f"(assert (= {x1} {x2}))")
        num1 = re.findall(r'\d+', x1)
        num2 = re.findall(r'\d+', x2)
        result_SPG.append(f"e || {num1[0]} || {num2[0]} || -1")

    #gen smt2
    with open(f'./Input/smt2_UnionFind/0/merge{j}.smt2', 'w') as f:
        f.write("(echo \"start\")\n")
        f.write("(set-logic QF_UF)\n")
        f.write("(declare-sort A 0)\n")
        for var in var_declar:
            f.write(f"(declare-const {var} A)\n")
        for stmt in result_logic:
            f.write(stmt + "\n")
        f.write("(check-sat)\n")
        f.write("(echo \"f_solved_time:\")\n")

    # gen SPG
    with open(f'./Input/SPG_UnionFind/0/merge{j}.spg', 'w') as f5:
        for stmt in result_SPG:
            f5.write(stmt + "\n")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Timecost: {elapsed_time:.2f} s")

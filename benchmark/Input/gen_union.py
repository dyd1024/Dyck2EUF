import random

def generate_variable_pairs(num_vars=50000, pair_counts=[5000, 10000, 15000, 20000, 25000], seed=42):
    # random.seed(seed)

    for count in pair_counts:
        print(f"Generating {count} variable pairs...")
        pairs_set = set()
        pairs_graph_set = set()
        var_set = set()

        max_attempts = int(count * 1.2)
        attempts = 0

        while len(pairs_set) < count and attempts < max_attempts:
            i, j = random.sample(range(num_vars), 2)
            if i > j:
                i, j = j, i
            pairs_set.add((f"x{i}", f"x{j}"))
            pairs_graph_set.add((f"{i}", f"{j}"))
            var_set.add(f"x{i}")
            var_set.add(f"x{j}")
            attempts += 1

        if len(pairs_set) < count:
            while len(pairs_set) < count:
                i, j = random.sample(range(num_vars), 2)
                if i > j:
                    i, j = j, i
                pairs_set.add((f"x{i}", f"x{j}"))
                var_set.add(f"x{i}")
                var_set.add(f"x{j}")

        pairs_list = list(pairs_set)
        var_list = list(var_set)

        with open(f"./smt2_unionfind/0/unionfind_{count}.smt2", 'w', encoding="utf-8") as f:
            f.write("(echo \"start\")\n")
            f.write("(set-logic QF_UF)\n")
            f.write("(declare-sort A 0)\n")
            for var in var_list:
                f.write(f"(declare-const {var} A)\n")
            for a, b in pairs_list:
                f.write(f"(assert (= {a} {b}))\n")
            f.write("(echo \"f_parser_time:\")\n")
            f.write("(check-sat)\n")
            f.write("(echo \"f_solved_time:\")\n")
        with open(f"./SPG_unionfind/0/unionfind_{count}.spg", 'w', encoding="utf-8") as f_graph:
            for a, b in pairs_graph_set:
                f_graph.write(f"e || {a} || {b} || -1\n")

if __name__ == "__main__":
    generate_variable_pairs()
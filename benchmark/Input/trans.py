import re
import random
import time
import os

AliasAnalysis=[
    'antlr', 'bloat', 'chart', 'eclipse', 'fop', 'hsqldb', 'jython', 'luindex', 'lusearch', 'pmd', 'xalan'
]

AliasAnalysis_C=[
    'git', 'libssh2.a', 'tmux', 'vim', 'lighttpd', 'sqlite3', 'strace', 'wrk', 'darknet', 'libxml2.a'
]

DataDep = [
    'btree', 'check', 'compiler', 'compress', 'crypto', 'derby', 'helloworld', 'mpegaudio', 'mushroom', 'parser', 'sample', 'scimark', 'startup', 'sunflow', 'xml'
]

query_len = 11

analysis_Type = [
    "AliasAnalysis",
    "AliasAnalysis_C",
    "DataDepAnalysis"
]

start_time = time.time()

for analysisType in analysis_Type:
    if analysisType == "AliasAnalysis":
        benchmarks = AliasAnalysis
    elif analysisType == "DataDepAnalysis":
        benchmarks = DataDep
    elif analysisType == "AliasAnalysis_C":
        benchmarks = AliasAnalysis_C

    # get results
    for bm in benchmarks:
        node_set = set()
        edges_num = 0
        label_set = set()
        function_declar = set()
        var_declar = set()
        var_map = {}
        result_logic = []
        result_SPG = []
        with open(f'../Dot/{analysisType}/{bm}.dot', 'r') as f0:
            var_num = 0
            for line in f0:
                #  line = "17300->1780425009[label=\"op--1173\"]"
                pattern = r"\d+"
                if '[' in line:
                    matchs = re.findall(pattern, line)
                    assert (len(matchs) == 3)
                    node_set.add(matchs[0])
                    node_set.add(matchs[1])
                    edges_num += 1
                    label_set.add(matchs[2])

                    if var_map.get(matchs[0]) == None:
                        var_map.update({matchs[0]: var_num})
                        var_num += 1
                    if var_map.get(matchs[1]) == None:
                        var_map.update({matchs[1]: var_num})
                        var_num += 1

                    var_declar.add("x" + str(var_map[matchs[0]]))
                    var_declar.add("x" + str(var_map[matchs[1]]))
                    function_declar.add("f" + matchs[2])

                    result_logic.append(f"(assert (= x{var_map.get(matchs[0])} (f{matchs[2]} x{var_map.get(matchs[1])})))")
                    result_SPG.append(f"e || {var_map.get(matchs[1])} || {var_map.get(matchs[0])} || {matchs[2]}")


        with open(f'./SPG_{analysisType}/0/{bm}.spg', 'w') as f5:
            for stmt in result_SPG:
                f5.write(stmt + "\n")
        os.system(f'./get_result ./SPG_{analysisType}/0/{bm}.spg ./SPG_{analysisType}/0/{bm}.seq  > ../Dot/{analysisType}_result/{bm}.result')

        print(f'=============================== Generate query pairs [{analysisType}:{bm}] ===============================\n')
        print(f'=========================={bm}:[node_num:{str(len(node_set))}] [edge_num:{str(edges_num)}] [label_num:{str(len(label_set))}]==========================\n')

        for j in range(query_len):
            seq_length = j*1000
            print("query length:" + str(seq_length))
            results = []
            query = []
            with open(f'../Dot/{analysisType}_result/{bm}.result', 'r') as f_temp:
                for line in f_temp:
                    pattern = r"\d+"
                    matchs = re.findall(pattern, line)
                    if(len(matchs) == 2):
                        if(matchs[0] != matchs[1]):
                            results.append([matchs[0],matchs[1]])

            i = 0
            while i < seq_length:
                 if random.random() < 0.5:
                     query1 = random.choice(list(var_declar))
                     query2 = random.choice(list(var_declar))

                     if query1 != query2:
                        i = i+1
                        query.append([str(query1), str(query2)])
                 else:
                     query_temp = random.choice(list(results))
                     x1 = query_temp[0]
                     x2 = query_temp[1]
                     if x1==None or x2==None:
                         print(query_temp[0],query_temp[1])
                     assert(x1 != None and x2 != None)
                     query1 = "x" + str(x1)
                     query2 = "x" + str(x2)
                     query.append([query1, query2])
                     i = i+1

        #dot2smt2
            with open(f'./smt2_{analysisType}/{seq_length}/{bm}.smt2', 'w') as f2:
                f2.write("(echo \"start\")\n")
                f2.write("(set-logic QF_UF)\n")
                f2.write("(declare-sort A 0)\n")
                for var in var_declar:
                    f2.write(f"(declare-const {var} A)\n")
                for fun in function_declar:
                    f2.write(f"(declare-fun {fun} (A) A)\n")
                for stmt in result_logic:
                    f2.write(stmt+"\n")
                f2.write("(echo \"f_parser_time:\")\n")
                if j == 0:
                    x1 = random.choice(list(var_declar))
                    x2 = random.choice(list(var_declar))
                    f2.write(f"(assert (not (= {x1} {x2})))\n")
                f2.write("(check-sat)\n")
                f2.write("(echo \"f_solved_time:\")\n")
                for a in query:
                    f2.write("(push 1)\n")
                    f2.write(f"(assert (not (= {a[0]} {a[1]})))\n")
                    f2.write("(check-sat)\n")
                    f2.write("(pop 1)\n")
                f2.write("(echo \"query_time:\")\n")

        #dot2SPG
            # if j==0:
            #     with open(f'./Input/SPG_{analysisType}/0/{bm}.spg', 'w') as f5:
            #         for stmt in result_SPG:
            #             f5.write(stmt+"\n")

            with open(f'./SPG_{analysisType}/{seq_length}/{bm}.seq', 'w') as f6:
                for a in query:
                    f6.write(f"q || {a[0][1:]} || {a[1][1:]}\n")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Timecost: {elapsed_time:.2f} s")

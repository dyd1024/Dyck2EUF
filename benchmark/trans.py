import re
import random

AliasAnalysis=[
'antlr',
'bloat',
'chart',
'eclipse',
'fop',
'hsqldb',
'jython',
'luindex',
'lusearch',
'pmd',
'xalan'
]

DataDep = [
'btree',
'check',
'compiler',
'compress',
'crypto',
'derby',
'helloworld',
'mpegaudio',
'mushroom',
'parser',
'sample',
'scimark',
'startup',
'sunflow',
'xml'
]

analysis_Type = [
    "AliasAnalysis",
    "DataDepAnalysis"
]
for analysisType in analysis_Type:
    if analysisType == "AliasAnalysis":
        benchmarks = AliasAnalysis
    elif analysisType == "DataDepAnalysis":
        benchmarks = DataDep

    for j in range(11):
        seq_length = j*1000
        for bm in benchmarks:
            results = []
            with open(f'./{analysisType}_result/{bm}.result', 'r') as f_temp:
                for line in f_temp:
                    pattern = r"\d+"
                    matchs = re.findall(pattern, line)
                    if(len(matchs) == 2):
                        if(matchs[0] != matchs[1]):
                            results.append([matchs[0],matchs[1]])

            function_declar = set()
            var_declar = set()
            result_logic = []
            result_SPG = []

            var_map = {}
            query = []

            with open(f'./{analysisType}/{bm}.dot', 'r') as f0:
                 var_num = 0
                 for line in f0:
                    #  line = "17300->1780425009[label=\"op--1173\"]"
                     pattern = r"\d+"
                     matchs = re.findall(pattern, line)
                     assert len(matchs) == 3
                     var_declar.add("x"+matchs[0])
                     var_declar.add("x"+matchs[1])
                     if var_map.get(matchs[0]) == None:
                        var_map.update({matchs[0]:var_num})
                        var_num += 1
                     if var_map.get(matchs[1]) == None:
                        var_map.update({matchs[1]:var_num})
                        var_num += 1
                     if var_map.get(matchs[2]) == None:
                        var_map.update({matchs[2]:var_num})
                        var_num += 1

                     function_declar.add("f"+matchs[2])
                     result_logic.append( f"(assert (= x{matchs[0]} (f{matchs[2]} x{matchs[1]} ) ))")
                     result_SPG.append(f"e || {matchs[1]} || {matchs[0]} || {matchs[2]}")

                 i = 0
                 while i < seq_length:
                     if random.random() < 0.5:
                         query1 = random.sample(var_declar, 1)
                         query2 = random.sample(var_declar, 1)
                         if query1 != query2:
                            i = i+1
                            query.append([query1[0], query2[0]])
                     else:
                         query_temp = random.sample(results, 1)
                         query1 = "x" + query_temp[0][0]
                         query2 = "x" + query_temp[0][1]
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
                f2.write("(check-sat)\n")
                f2.write("(echo \"f_solved_time:\")\n")
                for a in query:
                    f2.write("(push 1)\n")
                    f2.write(f"(assert (not (= {a[0]} {a[1]})))\n")
                    f2.write("(check-sat)\n")
                    f2.write("(pop 1)\n")
                f2.write("(echo \"query_time:\")\n")


        #dot2SPG
            if j==0:
                with open(f'./SPG_{analysisType}/{seq_length}/{bm}.spg', 'w') as f5:
                    for stmt in result_SPG:
                        f5.write(stmt+"\n")

            with open(f'./SPG_{analysisType}/{seq_length}/{bm}.seq', 'w') as f6:
                for a in query:
                    a1 = a[0][1:]
                    a2 = a[1][1:]
                    f6.write(f"q || {a1} || {a2}\n")

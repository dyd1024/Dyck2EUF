import re
import random
import time

AliasAnalysis=[
    'antlr', 'bloat', 'chart', 'eclipse', 'fop', 'hsqldb', 'jython', 'luindex', 'lusearch', 'pmd', 'xalan'
]

AliasAnalysis_C=[
    'git', 'libssh2.a', 'tmux', 'vim', 'lighttpd', 'sqlite3', 'strace', 'wrk', 'darknet', 'libxml2.a'
]

DataDep = [
    'btree', 'check', 'compiler', 'compress', 'crypto', 'derby', 'helloworld', 'mpegaudio', 'mushroom', 'parser', 'sample', 'scimark', 'startup', 'sunflow', 'xml'
]

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

    for j in range(2):
        seq_length = j*1000
        print("query length:" + str(seq_length))
        for bm in benchmarks:
            print(bm)
            results = []
            with open(f'../Dot/{analysisType}_result/{bm}.result', 'r') as f_temp:
                for line in f_temp:
                    pattern = r"\d+"
                    matchs = re.findall(pattern, line)
                    if(len(matchs) == 2):
                        if(matchs[0] != matchs[1]):
                            results.append([matchs[0],matchs[1]])

            var_declar = set()

            var_map = {}
            query = []

            # ====================================================================================================
            # result_muz = []
            result_bdd = []
            result_dl = []
            # ====================================================================================================

            with open(f'../Dot/{analysisType}/{bm}.dot', 'r') as f0:
                 var_num = 0
                 for line in f0:
                    #  line = "17300->1780425009[label=\"op--1173\"]"
                     pattern = r"\d+"
                     matchs = re.findall(pattern, line)
                     if(len(matchs) != 3):
                         continue
                     else:
                         if var_map.get(matchs[0]) == None:
                            var_map.update({matchs[0]:var_num})
                            var_num += 1
                         if var_map.get(matchs[1]) == None:
                            var_map.update({matchs[1]:var_num})
                            var_num += 1
                         # if var_map.get(matchs[2]) == None:
                         #    var_map.update({matchs[2]:var_num})
                         #    var_num += 1
                         var_declar.add("x" + str(var_map[matchs[0]]))
                         var_declar.add("x" + str(var_map[matchs[1]]))

                         m0 = var_map.get(matchs[0])
                         m1 = var_map.get(matchs[1])
                         # m2 = var_map.get(matchs[2])
                         # m_0f = format(m0,'016b')
                         # m_1f = format(m1,'016b')
                         # m_2f = format(m2,'016b')
                         # result_muz.append(f'(rule (fun #b{m_0f} #b{m_2f} #b{m_1f}))\n')
                         result_bdd.append(f'fun({m0}, {int(matchs[2])}, {m1}).\n')
                         result_dl.append(f'fun({m0}, {int(matchs[2])}, {m1}).\n')
                 i = 0
                 while i < seq_length:
                     if random.random() < 0.5:
                         query1 = random.choice(list(var_declar))
                         query2 = random.choice(list(var_declar))
                         if query1 != query2:
                            i = i+1
                            query.append([str(query1), str(query2)])
                     else:
                         # query_temp = random.sample(results, 1)
                         query_temp = random.choice(list(results))
                         query1 = "x" + str(var_map.get(query_temp[0]))
                         query2 = "x" + str(var_map.get(query_temp[1]))
                         query.append([query1, query2])
                         i = i+1

        #dot2bdd
            with open(f'./bdd_{analysisType}/{seq_length}/{bm}.datalog', 'w') as f8:
                f8.write(f"Z {var_num+1}\n")
                f8.write("eq(x : Z, y : Z) printsize\n")
                f8.write("fun(x : Z, f : Z, y : Z)\n")
                f8.write("eq(x, y) :- eq(y, x).\n")
                f8.write("eq(x, z) :- eq(x, y), eq(y, z).\n")
                f8.write("fun(x, f, z) :- fun(x, f, y), eq(z, y).\n")
                f8.write("eq(x, y) :- fun(x, f, z), fun(y, f, z).\n")
                for item in result_bdd:
                    f8.write(item)
                que_1 = 0
                for a in query:
                    f8.write(f'q{que_1}(x : Z, y : Z) printsize\n')
                    f8.write(f'q{que_1}(x, y) :- eq(x, y), x = {a[0][1:]}, y = {a[1][1:]}.\n')
                    que_1 = que_1+1
        #dot2dl
            with open(f'./dl_{analysisType}/{seq_length}/{bm}.dl', 'w') as f9:
                f9.write(".decl eq(x: number, y: number)\n")
                f9.write(".decl fun(x: number, f: number, y:number)\n")
                f9.write("eq(x, y) :- eq(y, x).\n")
                f9.write("eq(x, z) :- eq(x, y), eq(y, z).\n")
                f9.write("fun(x, f, z) :- fun(x, f, y), eq(z, y).\n")
                f9.write("eq(x, y) :- fun(x, f, z), fun(y, f, z).\n")
                for line in result_dl:
                    f9.write(line)
                f9.write(".decl iseq(x: number, y: number)\n")
                f9.write(f".output iseq(filename=\"{bm}_res.csv\")\n")
                for a in query:
                    f9.write(f"iseq(x, y) :- eq(x, y), x={a[0][1:]}, y={a[1][1:]}.\n")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Timecost: {elapsed_time:.2f} s")
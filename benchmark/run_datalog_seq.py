import time
import subprocess

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

alias_num = len(AliasAnalysis)
alias_C_num = len(AliasAnalysis_C)
data_num = len(DataDep)

bdd_alias_time = [0.0]*alias_num
bdd_alias_C_time = [0.0]*alias_C_num
bdd_dd_time = [0.0]*data_num

bdd_alias_time_query = [0.0]*alias_num
bdd_alias_C_time_query = [0.0]*alias_C_num
bdd_dd_time_query = [0.0]*data_num

souffle_alias_time = [0.0]*alias_num
souffle_alias_C_time = [0.0]*alias_C_num
souffle_dd_time = [0.0]*data_num

souffle_alias_time_query = [0.0]*alias_num
souffle_alias_C_time_query = [0.0]*alias_C_num
souffle_dd_time_query = [0.0]*data_num

times = 3
start_time = time.time()

for analysisType in analysis_Type:
    if analysisType == "AliasAnalysis":
        benchmarks = AliasAnalysis
    elif analysisType == "DataDepAnalysis":
        benchmarks = DataDep
    elif analysisType == "AliasAnalysis_C":
        benchmarks = AliasAnalysis_C
    for j in range(2):
        for num in range(times):
            bm_num = 0
            for bm in benchmarks:
                tm1 = False
                oom1 = False
                if j==0:
                    print("bddbddb-"+bm+f":analysis round {num+1}")
                else:
                    print("bddbddb-" + bm + f":query round {num+1}")
                time_start = time.time()
                #os.system(f"java -jar ../bddbddb_test/bddbddb-full.jar ./bdd_{analysisType}/{j*1000}/{bm}.datalog")
                with open(f'./datalog_result/bddbddb/{j*1000}/{bm}.res', 'w') as outfile:
                    try:
                        process = subprocess.Popen(
                            ['java', '-jar', '../bddbddb_test/bddbddb-full.jar', f'./Input/bdd_{analysisType}/{j * 1000}/{bm}.datalog' ],
                            stdout=outfile,
                            stderr=subprocess.PIPE)
                        stdout, stderr = process.communicate(timeout=600)
                        if b'OutOfMemoryError' in stderr:
                            oom1 = True
                            print("OUTofMemory")
                    except subprocess.TimeoutExpired:
                        process.kill()
                        tm1 = True
                        print("TimeOut")
                    except Exception as e:
                        print(f"error: {e}")
                time_end = time.time()
                print(time_end - time_start)
                time_mapping = {
                    0: {
                        "AliasAnalysis": bdd_alias_time,
                        "AliasAnalysis_C": bdd_alias_C_time,
                        "DataDepAnalysis": bdd_dd_time,
                    },
                    1: {
                        "AliasAnalysis": bdd_alias_time_query,
                        "AliasAnalysis_C": bdd_alias_C_time_query,
                        "DataDepAnalysis": bdd_dd_time_query,
                    }
                }

                if j in time_mapping and analysisType in time_mapping[j]:
                    time_var = time_mapping[j][analysisType]

                    if tm1 == False:
                        time_var[bm_num] += time_end - time_start
                    else:
                        time_var[bm_num] += 1800

                    if oom1 == True or time_var[bm_num] == 0.1:
                        time_var[bm_num] = 0.1

                if j==0:
                    print("souffle-"+bm+f":analysis round {num+1}")
                else:
                    print("souffle-" + bm + f":query round {num+1}")
                tm2 = False
                oom2 = False
                time_start = time.time()
                command = [
                    "../souffle_test/souffle",
                    "-D", f"./datalog_result/souffle/{j * 1000}/",
                    f"./Input/dl_{analysisType}/{j * 1000}/{bm}.dl"
                ]
                try:
                    process = subprocess.Popen(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    stdout, stderr = process.communicate(timeout=600)
                    if b'OutOfMemoryError' in stderr:
                        oom2 = True
                        print("OUTofMEmory")
                except subprocess.TimeoutExpired:
                    process.kill()
                    tm2 = True
                    print("TimeOut")
                except Exception as e:
                    print(f"error: {e}")
                time_end = time.time()
                print(time_end - time_start)

                time_mapping = {
                    0: {
                        "AliasAnalysis": souffle_alias_time,
                        "AliasAnalysis_C": souffle_alias_C_time,
                        "DataDepAnalysis": souffle_dd_time,
                    },
                    1: {
                        "AliasAnalysis": souffle_alias_time_query,
                        "AliasAnalysis_C": souffle_alias_C_time_query,
                        "DataDepAnalysis": souffle_dd_time_query,
                    }
                }

                if j in time_mapping and analysisType in time_mapping[j]:
                    time_var = time_mapping[j][analysisType]

                    if tm2 is False:
                        time_var[bm_num] += time_end - time_start
                    else:
                        time_var[bm_num] += 1800

                    if oom2 or time_var[bm_num] == 0.1:
                        time_var[bm_num] = 0.1
                print("===============================")
                bm_num += 1


with open('./datalog_result/result.txt', 'w') as f_out:
    output_config = [
        ("bddbddb alias analysis time:\n", bdd_alias_time),
        ("bddbddb alias analysis query time:\n", bdd_alias_time_query),
        ("souffle alias analysis time:\n", souffle_alias_time),
        ("souffle alias analysis query time:\n", souffle_alias_time_query),

        ("bddbddb alias_C analysis time:\n", bdd_alias_C_time),
        ("bddbddb alias_C analysis query time:\n", bdd_alias_C_time_query),
        ("souffle alias_C analysis time:\n", souffle_alias_C_time),
        ("souffle alias_C analysis query time:\n", souffle_alias_C_time_query),

        ("bdd data dependence analysis time:\n", bdd_dd_time),
        ("bdd data dependence analysis query time:\n", bdd_dd_time_query),
        ("souffle data dependence analysis:\n", souffle_dd_time),
        ("souffle data dependence analysis query time:\n", souffle_dd_time_query),
    ]

    for title, data_list in output_config:
        f_out.write(title)
        for item in data_list:
            if item == 0.1:
                f_out.write("OOM\n")
            elif item >= 1800:
                f_out.write("TimeOut\n")
            else:
                f_out.write(f"{round(item / times, 4)}\n")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Timecost: {elapsed_time:.2f} s")

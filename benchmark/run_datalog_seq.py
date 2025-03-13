import time
import os
import subprocess
import shlex

from duplicity.config import timeout

bdd_alias_time = [0.0]*11
bdd_dd_time = [0.0]*15

bdd_alias_time_query = [0.0]*11
bdd_dd_time_query = [0.0]*15

souffle_alias_time = [0.0]*11
souffle_dd_time = [0.0]*15

souffle_alias_time_query = [0.0]*11
souffle_dd_time_query = [0.0]*15

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
    for j in range(2):
        for num in range(3):
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
                            ['java', '-jar', '../bddbddb_test/bddbddb-full.jar', f'./bdd_{analysisType}/{j * 1000}/{bm}.datalog' ],
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
                if j == 0 and analysisType == "AliasAnalysis":
                    if tm1 == False:
                        bdd_alias_time[bm_num] += time_end - time_start
                    else:
                        bdd_alias_time[bm_num] += 1800
                    if oom1 == True:
                        bdd_alias_time[bm_num] = 0
                if j == 0 and analysisType == "DataDepAnalysis":
                    if tm1 == False:
                        bdd_dd_time[bm_num] += time_end - time_start
                    else:
                        bdd_dd_time[bm_num] += 1800
                    if oom1 == True:
                        bdd_dd_time[bm_num] = 0
                if j == 1 and analysisType == "AliasAnalysis":
                    if tm1 == False:
                        bdd_alias_time_query[bm_num] += time_end - time_start
                    else:
                        bdd_alias_time_query[bm_num] += 1800
                    if oom1 == True:
                        bdd_alias_time_query[bm_num] = 0
                if j == 1 and analysisType == "DataDepAnalysis":
                    if tm1 == False:
                        bdd_dd_time_query[bm_num] += time_end - time_start
                    else:
                        bdd_dd_time_query[bm_num] += 1800
                    if oom1 == True:
                        bdd_dd_time_query[bm_num] = 0
                print("===============================")

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
                    f"./dl_{analysisType}/{j * 1000}/{bm}.dl"
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
                if j == 0 and analysisType == "AliasAnalysis":
                    if tm2 == False:
                        souffle_alias_time[bm_num] += time_end - time_start
                    else:
                        souffle_alias_time[bm_num] += 1800
                    if oom2 == True:
                        souffle_alias_time[bm_num] = 0
                if j == 0 and analysisType == "DataDepAnalysis":
                    if tm2 == False:
                        souffle_dd_time[bm_num] += time_end - time_start
                    else:
                        souffle_dd_time[bm_num] += 1800
                    if oom2 == True:
                        souffle_dd_time[bm_num] = 0
                if j == 1 and analysisType == "AliasAnalysis":
                    if tm2 == False:
                        souffle_alias_time_query[bm_num] += time_end - time_start
                    else:
                        souffle_alias_time_query[bm_num] += 1800
                    if oom2 == True:
                        souffle_alias_time_query[bm_num] = 0
                if j == 1 and analysisType == "DataDepAnalysis":
                    if tm2 == False:
                        souffle_dd_time_query[bm_num] += time_end - time_start
                    else:
                        souffle_dd_time_query[bm_num] += 1800
                    if oom2 == True:
                        souffle_dd_time_query[bm_num] = 0
                print("===============================")
                bm_num += 1

with open(f'./datalog_result/result.txt','w') as f_out:
    f_out.write("bddbddb alias analysis time:\n")
    for item in bdd_alias_time:
        if item == 0:
            f_out.write("OOM\n")
        else:
            if item < 1800:
                f_out.write(f"{round(item/3, 4)}\n")
            else:
                f_out.write("TimeOut\n")
    f_out.write("bddbddb alias analysis query time:\n")
    for item in bdd_alias_time_query:
        if item == 0:
            f_out.write("OOM\n")
        else:
            if item < 1800:
                f_out.write(f"{round(item/3, 4)}\n")
            else:
                f_out.write("TimeOut\n")
    f_out.write("souffle alias analysis time:\n")
    for item in souffle_alias_time:
        if item == 0:
            f_out.write("OOM\n")
        else:
            if item < 1800:
                f_out.write(f"{round(item/3, 4)}\n")
            else:
                f_out.write("TimeOut\n")
    f_out.write("souffle alias analysis query time:\n")
    for item in souffle_alias_time_query:
        if item == 0:
            f_out.write("OOM\n")
        else:
            if item < 1800:
                f_out.write(f"{round(item/3, 4)}\n")
            else:
                f_out.write("TimeOut\n")
    f_out.write("bdd data dependence analysis time:\n")
    for item in bdd_dd_time:
        if item == 0:
            f_out.write("OOM\n")
        else:
            if item < 1800:
                f_out.write(f"{round(item/3, 4)}\n")
            else:
                f_out.write("TimeOut\n")
    f_out.write("bdd data dependence analysis query time:\n")
    for item in bdd_dd_time_query:
        if item == 0:
            f_out.write("OOM\n")
        else:
            if item < 1800:
                f_out.write(f"{round(item/3, 4)}\n")
            else:
                f_out.write("TimeOut\n")
    f_out.write("souffle data dependence analysis:\n")
    for item in souffle_dd_time:
        if item == 0:
            f_out.write("OOM\n")
        else:
            if item < 1800:
                f_out.write(f"{round(item/3, 4)}\n")
            else:
                f_out.write("TimeOut\n")
    f_out.write("souffle data dependence analysis query time:\n")
    for item in souffle_dd_time_query:
        if item == 0:
            f_out.write("OOM\n")
        else:
            if item < 1800:
                f_out.write(f"{round(item/3, 4)}\n")
            else:
                f_out.write("TimeOut\n")

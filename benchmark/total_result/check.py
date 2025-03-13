import os
import time
import sys
import re
import random
import csv

AnalysisType = [
'AliasAnalysis',
'DataDepAnalysis'
]

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

def find_floats(string):
    return re.findall(r'\b[-+]?\d+(\.\d+)?(?:[eE][-+]?\d+)?\b', string)


#cvc5
for step in range(11):
    cvc5_alias_res = []
    cvc5_dd_res = []
    start = 0
    for analysisType in AnalysisType:
            with open(f'../../cvc5_test/result/{step*1000}/{analysisType}{0}.res', 'r') as f1:
                 for line in f1:
                     if "f_solved_time" in line:
                         start = 1
                     if "start" in line:
                         start = 0
                     if analysisType == "AliasAnalysis":
                        if "unsat" in line and start == 1:
                            cvc5_alias_res.append(0)
                        if ("sat" in line) and (not ("un" in line)) and (start == 1) :
                            cvc5_alias_res.append(1)
                     if analysisType == "DataDepAnalysis" and start == 1:
                        if "unsat" in line:
                            cvc5_dd_res.append(0)
                        if ("sat" in line) and (not ("un" in line)) :
                            cvc5_dd_res.append(1)


    #optimal
    optimal_alias_res = []
    optimal_dd_res = []
    for analysisType in AnalysisType:
            with open(f'../../optimal_test/result/{step*1000}/{analysisType}{0}.res', 'r') as f2:
                 for line in f2:
                     if analysisType == "AliasAnalysis":
                         if ("Reachability" in line) and (not ("not" in line)) :
                            optimal_alias_res.append(0)
                         if ("not Reachability" in line) :
                            optimal_alias_res.append(1)
                     if analysisType == "DataDepAnalysis":
                         if ("Reachability" in line) and (not ("not" in line)) :
                            optimal_dd_res.append(0)
                         if ("not Reachability" in line):
                            optimal_dd_res.append(1)

    #fastDyck
    fastDyck_alias_res = []
    fastDyck_dd_res = []
    for analysisType in AnalysisType:
            with open(f'../../fastDyck_test/result/{step*1000}/{analysisType}{0}.res', 'r') as f2:
                 for line in f2:
                     if analysisType == "AliasAnalysis":
                         if ("Reachability" in line) and (not ("not" in line)) :
                            fastDyck_alias_res.append(0)
                         if ("not Reachability" in line) :
                            fastDyck_alias_res.append(1)
                     if analysisType == "DataDepAnalysis":
                         if ("Reachability" in line) and (not ("not" in line)) :
                            fastDyck_dd_res.append(0)
                         if ("not Reachability" in line):
                            fastDyck_dd_res.append(1)

    #platsmt
    platsmt_alias_res = []
    platsmt_dd_res = []
    start = 0
    for analysisType in AnalysisType:
            with open(f'../../platsmt_test/result/{step*1000}/{analysisType}{0}.res', 'r') as f3:
                 for line in f3:
                     if "f_solved_time" in line:
                         start = 1
                     if "start" in line:
                         start = 0
                     if analysisType == "AliasAnalysis":
                        if "unsat" in line and start == 1:
                            platsmt_alias_res.append(0)
                        if ("sat" in line) and (not ("un" in line)) and (start == 1) :
                            platsmt_alias_res.append(1)
                     if analysisType == "DataDepAnalysis":
                        if "unsat" in line and start == 1:
                            platsmt_dd_res.append(0)
                        if ("sat" in line) and (not ("un" in line)) and (start == 1) :
                            platsmt_dd_res.append(1)

    #yices

    yices_alias_res = []
    yices_dd_res = []
    start = 0
    for analysisType in AnalysisType:
            with open(f'../../Yices_test/result/{step*1000}/{analysisType}{0}.res', 'r') as f4:
                 for line in f4:
                     if "f_solved_time" in line:
                         start = 1
                     if "query_time" in line:
                         start = 0
                     if analysisType == "AliasAnalysis":
                        if "unsat" in line and start == 1:
                            yices_alias_res.append(0)
                        if ("sat" in line) and (not ("un" in line)) and (start == 1) :
                            yices_alias_res.append(1)
                     if analysisType == "DataDepAnalysis":
                        if "unsat" in line and start == 1:
                            yices_dd_res.append(0)
                        if ("sat" in line) and (not ("un" in line)) and (start == 1) :
                            yices_dd_res.append(1)

    #z3
    z3_alias_res = []
    z3_dd_res = []
    start = 0
    for analysisType in AnalysisType:
            with open(f'../../z3_test/result/{step*1000}/{analysisType}{0}.res', 'r') as f5:
                 for line in f5:
                     if "f_solved_time" in line:
                         start = 1
                     if "start" in line:
                         start = 0
                     if analysisType == "AliasAnalysis" and start == 1:
                         if "unsat" in line:
                            z3_alias_res.append(0)
                         if ("sat" in line) and (not ("un" in line)) and (start == 1) :
                            z3_alias_res.append(1)
                     if analysisType == "DataDepAnalysis" :
                         if "unsat" in line and start == 1:
                            z3_dd_res.append(0)
                         if ("sat" in line) and (not ("un" in line)) and (start == 1) :
                            z3_dd_res.append(1)
    i = 0
    flag = 0
    for x in optimal_alias_res:
        if ( x != fastDyck_alias_res[i] or x != yices_alias_res[i] or x!=z3_alias_res[i] or x!=cvc5_alias_res[i] or x!=platsmt_alias_res[i] ):
            flag = 1
        i = i + 1

    j = 0
    for x in optimal_dd_res:
        if ( x != fastDyck_dd_res[j] or x!=z3_dd_res[j] or x!=cvc5_dd_res[j] or x!=platsmt_dd_res[j] ):
            flag = 1
        j = j + 1

    if ( flag == 0 ):
        print("Consistency check passed")
    else:
        print("Consistency check failed")

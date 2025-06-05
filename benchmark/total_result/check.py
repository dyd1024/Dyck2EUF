import os
import time
import sys
import re
import random
import csv

analysis_Type = [
    "AliasAnalysis",
    "AliasAnalysis_C",
    "DataDepAnalysis"
]

AliasAnalysis=[
    'antlr', 'bloat', 'chart', 'eclipse', 'fop', 'hsqldb', 'jython', 'luindex', 'lusearch', 'pmd', 'xalan'
]

AliasAnalysis_C=[
    'git', 'libssh2.a', 'tmux', 'vim', 'lighttpd', 'sqlite3', 'strace', 'wrk', 'darknet', 'libxml2.a'
]

DataDep = [
    'btree', 'check', 'compiler', 'compress', 'crypto', 'derby', 'helloworld', 'mpegaudio', 'mushroom', 'parser', 'sample', 'scimark', 'startup', 'sunflow', 'xml'
]

# def find_floats(string):
#     pattern = r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'
#     return [match.group(0) for match in re.finditer(pattern, string)]

# 工具定义：名称 -> 路径模板、是否需要 start 标志
tools_config = {
    'optimal': {
        'path': '../../optimal_test/result/{}/{}0.res',
        'start_logic': False,
        'alias': [], 'alias_C': [], 'dd': []
    },
    'fastDyck': {
        'path': '../../fastDyck_test/result/{}/{}0.res',
        'start_logic': False,
        'alias': [], 'alias_C': [], 'dd': []
    },
    'platsmt': {
        'path': '../../platsmt_test/result/{}/{}0.res',
        'start_logic': True,
        'alias': [], 'alias_C': [], 'dd': []
    },
    'Yices': {
        'path': '../../Yices_test/result/{}/{}0.res',
        'start_logic': True,
        'alias': [], 'alias_C': [], 'dd': []
    },
    'z3': {
        'path': '../../z3_test/result/{}/{}0.res',
        'start_logic': True,
        'alias': [], 'alias_C': [], 'dd': []
    },
    'cvc5': {
        'path': '../../cvc5_test/result/{}/{}0.res',
        'start_logic': True,
        'alias': [], 'alias_C': [], 'dd': []
    }
}

for analysisType in analysis_Type:
    for step in range(10):
        for tool in tools_config.values():
            tool['alias'] = []
            tool['dd'] = []
            tool['alias_C'] = []

        for tool_name, config in tools_config.items():
            path_template = config['path']
            use_start_logic = config['start_logic']
            alias_list = config['alias']
            alias_C_list = config['alias_C']
            dd_list = config['dd']

            full_path = path_template.format((step+1) * 1000, analysisType)
            try:
                with open(full_path, 'r') as f:
                    start = 0
                    for line in f:
                        if use_start_logic:
                            if "f_solved_time" in line:
                                start = 1
                            if "start" in line or "query_time" in line:
                                start = 0

                        # AliasAnalysis
                        if analysisType == "AliasAnalysis":
                            if use_start_logic and start == 1:
                                if "unsat" in line:
                                    alias_list.append(0)
                                elif "sat" in line and "un" not in line:
                                    alias_list.append(1)
                            else:
                                if "Reachability" in line and "not" not in line:
                                    alias_list.append(0)
                                elif "not Reachability" in line:
                                    alias_list.append(1)
                        # AliasAnalysis_C
                        if analysisType == "AliasAnalysis_C":
                            if use_start_logic and start == 1:
                                if "unsat" in line:
                                    alias_C_list.append(0)
                                elif "sat" in line and "un" not in line:
                                    alias_C_list.append(1)
                            else:
                                if "Reachability" in line and "not" not in line:
                                    alias_C_list.append(0)
                                elif "not Reachability" in line:
                                    alias_C_list.append(1)

                        # DataDepAnalysis
                        if analysisType == "DataDepAnalysis":
                            if use_start_logic and start == 1:
                                if "unsat" in line:
                                    dd_list.append(0)
                                elif "sat" in line and "un" not in line:
                                    dd_list.append(1)
                            else:
                                if "Reachability" in line and "not" not in line:
                                    dd_list.append(0)
                                elif "not Reachability" in line:
                                    dd_list.append(1)

            except Exception as e:
                print(f"[ERROR] Reading {full_path}: {e}")

        all_alias_results = [tool['alias'] for tool in tools_config.values()]
        all_alias_C_results = [tool['alias_C'] for tool in tools_config.values()]
        all_dd_results = [tool['dd'] for tool in tools_config.values()]

        flag = 0
        reference_alias = all_alias_results[0]
        for result in all_alias_results[1:]:
            if result != reference_alias:
                flag = 1
                break

        reference_alias_C = all_alias_C_results[0]
        for result in all_alias_C_results[1:]:
            if result != reference_alias_C:
                flag = 1
                break

        reference_dd = all_dd_results[0]
        for result in all_dd_results[1:]:
            if result != reference_dd:
                flag = 1
                break

        if flag == 0:
            print("Consistency check passed")
        else:
            print("Consistency check failed")


















# #cvc5
# for step in range(11):
#     cvc5_alias_res = []
#     cvc5_dd_res = []
#     start = 0
#     for analysisType in analysis_Type:
#             with open(f'../../cvc5_test/result/{step*1000}/{analysisType}{0}.res', 'r') as f1:
#                  for line in f1:
#                      if "f_solved_time" in line:
#                          start = 1
#                      if "start" in line:
#                          start = 0
#                      if analysisType == "AliasAnalysis":
#                         if "unsat" in line and start == 1:
#                             cvc5_alias_res.append(0)
#                         if ("sat" in line) and (not ("un" in line)) and (start == 1) :
#                             cvc5_alias_res.append(1)
#                      if analysisType == "DataDepAnalysis" and start == 1:
#                         if "unsat" in line:
#                             cvc5_dd_res.append(0)
#                         if ("sat" in line) and (not ("un" in line)) :
#                             cvc5_dd_res.append(1)
#
#
#     #optimal
#     optimal_alias_res = []
#     optimal_dd_res = []
#     for analysisType in analysis_Type:
#             with open(f'../../optimal_test/result/{step*1000}/{analysisType}{0}.res', 'r') as f2:
#                  for line in f2:
#                      if analysisType == "AliasAnalysis":
#                          if ("Reachability" in line) and (not ("not" in line)) :
#                             optimal_alias_res.append(0)
#                          if ("not Reachability" in line) :
#                             optimal_alias_res.append(1)
#                      if analysisType == "DataDepAnalysis":
#                          if ("Reachability" in line) and (not ("not" in line)) :
#                             optimal_dd_res.append(0)
#                          if ("not Reachability" in line):
#                             optimal_dd_res.append(1)
#
#     #fastDyck
#     fastDyck_alias_res = []
#     fastDyck_dd_res = []
#     for analysisType in analysis_Type:
#             with open(f'../../fastDyck_test/result/{step*1000}/{analysisType}{0}.res', 'r') as f2:
#                  for line in f2:
#                      if analysisType == "AliasAnalysis":
#                          if ("Reachability" in line) and (not ("not" in line)) :
#                             fastDyck_alias_res.append(0)
#                          if ("not Reachability" in line) :
#                             fastDyck_alias_res.append(1)
#                      if analysisType == "DataDepAnalysis":
#                          if ("Reachability" in line) and (not ("not" in line)) :
#                             fastDyck_dd_res.append(0)
#                          if ("not Reachability" in line):
#                             fastDyck_dd_res.append(1)
#
#     #platsmt
#     platsmt_alias_res = []
#     platsmt_dd_res = []
#     start = 0
#     for analysisType in analysis_Type:
#             with open(f'../../platsmt_test/result/{step*1000}/{analysisType}{0}.res', 'r') as f3:
#                  for line in f3:
#                      if "f_solved_time" in line:
#                          start = 1
#                      if "start" in line:
#                          start = 0
#                      if analysisType == "AliasAnalysis":
#                         if "unsat" in line and start == 1:
#                             platsmt_alias_res.append(0)
#                         if ("sat" in line) and (not ("un" in line)) and (start == 1) :
#                             platsmt_alias_res.append(1)
#                      if analysisType == "DataDepAnalysis":
#                         if "unsat" in line and start == 1:
#                             platsmt_dd_res.append(0)
#                         if ("sat" in line) and (not ("un" in line)) and (start == 1) :
#                             platsmt_dd_res.append(1)
#
#     #yices
#
#     yices_alias_res = []
#     yices_dd_res = []
#     start = 0
#     for analysisType in analysis_Type:
#             with open(f'../../Yices_test/result/{step*1000}/{analysisType}{0}.res', 'r') as f4:
#                  for line in f4:
#                      if "f_solved_time" in line:
#                          start = 1
#                      if "query_time" in line:
#                          start = 0
#                      if analysisType == "AliasAnalysis":
#                         if "unsat" in line and start == 1:
#                             yices_alias_res.append(0)
#                         if ("sat" in line) and (not ("un" in line)) and (start == 1) :
#                             yices_alias_res.append(1)
#                      if analysisType == "DataDepAnalysis":
#                         if "unsat" in line and start == 1:
#                             yices_dd_res.append(0)
#                         if ("sat" in line) and (not ("un" in line)) and (start == 1) :
#                             yices_dd_res.append(1)
#
#     #z3
#     z3_alias_res = []
#     z3_dd_res = []
#     start = 0
#     for analysisType in analysis_Type:
#             with open(f'../../z3_test/result/{step*1000}/{analysisType}{0}.res', 'r') as f5:
#                  for line in f5:
#                      if "f_solved_time" in line:
#                          start = 1
#                      if "start" in line:
#                          start = 0
#                      if analysisType == "AliasAnalysis" and start == 1:
#                          if "unsat" in line:
#                             z3_alias_res.append(0)
#                          if ("sat" in line) and (not ("un" in line)) and (start == 1) :
#                             z3_alias_res.append(1)
#                      if analysisType == "DataDepAnalysis" :
#                          if "unsat" in line and start == 1:
#                             z3_dd_res.append(0)
#                          if ("sat" in line) and (not ("un" in line)) and (start == 1) :
#                             z3_dd_res.append(1)
#     i = 0
#     flag = 0
#     for x in optimal_alias_res:
#         if ( x != fastDyck_alias_res[i] or x != yices_alias_res[i] or x!=z3_alias_res[i] or x!=cvc5_alias_res[i] or x!=platsmt_alias_res[i] ):
#             flag = 1
#         i = i + 1
#
#     j = 0
#     for x in optimal_dd_res:
#         if ( x != fastDyck_dd_res[j] or x!=z3_dd_res[j] or x!=cvc5_dd_res[j] or x!=platsmt_dd_res[j] ):
#             flag = 1
#         j = j + 1
#
#     if ( flag == 0 ):
#         print("Consistency check passed")
#     else:
#         print("Consistency check failed")

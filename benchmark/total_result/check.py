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


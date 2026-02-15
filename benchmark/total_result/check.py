import os
import sys

analysis_Type = [
    "AliasAnalysis",
    "AliasAnalysis_C",
    "DataDepAnalysis"
]

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
    },
    'egg_R': {
        'path': '../../egg_R_test/result/{}/{}0.res',
        'start_logic': True,
        'alias': [], 'alias_C': [], 'dd': []
    }
}

# 提取 SMT 工具（start_logic 为 True）
smt_tools = {name: config for name, config in tools_config.items() if config['start_logic']}
optimal_config = tools_config['optimal']

for analysisType in analysis_Type:
    print(f"\n=== Analysis: {analysisType} ===")
    for step in range(10):
        size = (step + 1) * 1000
        # 清空结果
        optimal_config['alias'] = []
        optimal_config['alias_C'] = []
        optimal_config['dd'] = []
        for config in smt_tools.values():
            config['alias'] = []
            config['alias_C'] = []
            config['dd'] = []

        # 读取 optimal
        optimal_path = optimal_config['path'].format(size, analysisType)
        try:
            with open(optimal_path, 'r') as f:
                for line in f:
                    if analysisType == "AliasAnalysis":
                        if "Reachability" in line and "not" not in line:
                            optimal_config['alias'].append(0)
                        elif "not Reachability" in line:
                            optimal_config['alias'].append(1)
                    elif analysisType == "AliasAnalysis_C":
                        if "Reachability" in line and "not" not in line:
                            optimal_config['alias_C'].append(0)
                        elif "not Reachability" in line:
                            optimal_config['alias_C'].append(1)
                    else:  # DataDepAnalysis
                        if "Reachability" in line and "not" not in line:
                            optimal_config['dd'].append(0)
                        elif "not Reachability" in line:
                            optimal_config['dd'].append(1)
        except Exception as e:
            print(f"  [Step {step+1}] ERROR reading optimal: {e}")
            continue

        # 获取 reference
        ref = (
            optimal_config['alias'] if analysisType == "AliasAnalysis" else
            optimal_config['alias_C'] if analysisType == "AliasAnalysis_C" else
            optimal_config['dd']
        )

        if not ref:
            print(f"  [Step {step+1}] WARN: empty optimal result")
            continue

        inconsistent_tools = []
        for tool_name, config in smt_tools.items():
            tool_path = config['path'].format(size, analysisType)
            try:
                with open(tool_path, 'r') as f:
                    start = 0
                    for line in f:
                        if "f_solved_time" in line:
                            start = 1
                        if "start" in line or "query_time" in line:
                            start = 0

                        if analysisType == "AliasAnalysis" and start == 1:
                            if "unsat" in line:
                                config['alias'].append(0)
                            elif "sat" in line and "un" not in line:
                                config['alias'].append(1)
                        elif analysisType == "AliasAnalysis_C" and start == 1:
                            if "unsat" in line:
                                config['alias_C'].append(0)
                            elif "sat" in line and "un" not in line:
                                config['alias_C'].append(1)
                        elif analysisType == "DataDepAnalysis" and start == 1:
                            if "unsat" in line:
                                config['dd'].append(0)
                            elif "sat" in line and "un" not in line:
                                config['dd'].append(1)

                tool_res = (
                    config['alias'] if analysisType == "AliasAnalysis" else
                    config['alias_C'] if analysisType == "AliasAnalysis_C" else
                    config['dd']
                )

                if tool_res != ref:
                    inconsistent_tools.append(tool_name)

            except Exception as e:
                inconsistent_tools.append(tool_name)  # 文件缺失视为不一致

        if inconsistent_tools:
            print(f"  [Query length {(step+1)*1000}] FAIL: inconsistent with optimal – {', '.join(inconsistent_tools)}")
        else:
            print(f"  [Query length {(step+1)*1000}] PASS")

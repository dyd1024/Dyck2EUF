import re

AliasAnalysis=[
    'antlr', 'bloat', 'chart', 'eclipse', 'fop', 'hsqldb', 'jython', 'luindex', 'lusearch', 'pmd', 'xalan'
]

AliasAnalysis_C=[
    'git', 'libssh2.a', 'tmux', 'vim', 'lighttpd', 'sqlite3', 'strace', 'wrk', 'darknet', 'libxml2.a'
]

DataDep = [
    'btree', 'check', 'compiler', 'compress', 'crypto', 'derby', 'helloworld', 'mpegaudio', 'mushroom', 'parser', 'sample', 'scimark', 'startup', 'sunflow', 'xml'
]

alias_num = len(AliasAnalysis)
alias_C_num = len(AliasAnalysis_C)
data_num = len(DataDep)

def find_floats(string):
    pattern = r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'
    return [match.group(0) for match in re.finditer(pattern, string)]

tool_type = [
    'z3',
    'cvc5',
    'Yices'
]

analysis_Type = [
    "AliasAnalysis",
    "AliasAnalysis_C",
    "DataDepAnalysis"
]

graph_alias = []
yices_alias = []
platsmt_alias=[]

graph_alias_C = []
yices_alias_C = []
platsmt_alias_C=[]

graph_dd = []
yices_dd = []
platsmt_dd=[]

times = 3

#============================================================== get analysis time  ================================================================

for analysis in analysis_Type:
    with open(f'./{analysis}_result.txt', 'w') as f_temp:
        f_temp.write('')

    # graph_based_tools
    graph_tools = [
        ('FastDyck', '../../fastDyck_test/result/0/'),
        ('Optimal', '../../optimal_test/result/0/')
    ]
    for tool_name, base_path in graph_tools:
        file_prefix = f'{base_path}{analysis}'
        if analysis == 'AliasAnalysis':
            temp = [0.0] * alias_num
        elif analysis == 'AliasAnalysis_C':
            temp = [0.0] * alias_C_num
        elif analysis == 'DataDepAnalysis':
            temp = [0.0] * data_num
        # get solve time
        for i in range(times):
            with open(f'{file_prefix}{i}.res', 'r') as f:
                pro_num = 0
                for line in f:
                    if "Time of graph constructed" in line:
                        find_time = find_floats(line)
                        if find_time:
                            temp[pro_num] += float(find_time[0])
                            pro_num += 1

        with open(f'./{analysis}_result.txt', 'a') as fa:
            fa.write(f'{tool_name}\n')
            j = 1
            for item in temp:
                value = item * 1000 / times
                if tool_name == "Optimal" and analysis == 'AliasAnalysis':
                    graph_alias.append(value)
                elif tool_name == "Optimal" and analysis == 'AliasAnalysis_C':
                    value = item / times
                    graph_alias_C.append(value)
                elif tool_name == "Optimal" and analysis == 'DataDepAnalysis':
                    graph_dd.append(value)
                if tool_name == "FastDyck" and analysis == 'AliasAnalysis_C':
                    value = item / times
                fa.write(f'({j},{round(value, 3)}) ')
                j += 1
            fa.write('\n')

    # SMT_based tools
    tool_info = [
        ('z3', '../../z3_test/result/0/', False),
        ('cvc5', '../../cvc5_test/result/0/', False),
        ('Yices', '../../Yices_test/result/0/', False),
        ('plat-smt', '../../platsmt_test/result/0/', True),
    ]

    for tool_name, base_path, is_plat_smt in tool_info:
        if analysis == 'AliasAnalysis':
            temp = [0.0] * alias_num
        elif analysis == 'AliasAnalysis_C':
            temp = [0.0] * alias_C_num
        elif analysis == 'DataDepAnalysis':
            temp = [0.0] * data_num

        file_prefix = f'{base_path}{analysis}'

        for i in range(times):
            with open(f'{file_prefix}{i}.res', 'r') as f:
                pro_num = 0
                record_start = 0.0
                for line in f:
                    # plat-smt
                    if is_plat_smt:
                        if "start" in line and not ("startup" in line):
                            parts = line.split(":")
                            record_start = int(parts[1])
                        if "f_solved_time" in line:
                            parts = line.split(":")
                            current_time = int(parts[2])
                            temp[pro_num] += (current_time - record_start) / 1000
                            pro_num += 1
                    else:
                        if "f_solved_time" in line or "Time of graph constructed" in line:
                            find_time = find_floats(line)
                            if find_time:
                                temp[pro_num] += float(find_time[0])
                                pro_num += 1

        with open(f'./{analysis}_result.txt', 'a') as fa:
            fa.write(f'{tool_name}\n')
            j = 1
            for item in temp:
                if is_plat_smt:
                    if analysis == 'AliasAnalysis_C':
                        # Unit:seconds
                        value = round(item / (1000*times), 3)
                    else:
                        # Unit:milliseconds
                        value = round(item / times, 3)
                else:
                    if analysis == 'AliasAnalysis_C':
                        # Unit:seconds
                        value = round(item / times, 3)
                    else:
                        # Unit:milliseconds
                        value = round(item * 1000 / times, 3)

                fa.write(f'({j},{value}) ')

                if tool_name == "Yices" and analysis == 'AliasAnalysis':
                    yices_alias.append(value)
                if tool_name == "Yices" and analysis == 'AliasAnalysis_C':
                    yices_alias_C.append(value)
                if tool_name == "Yices" and analysis == 'DataDepAnalysis':
                    yices_dd.append(value)
                if tool_name == "plat-smt" and analysis == 'AliasAnalysis':
                    platsmt_alias.append(value)
                if tool_name == "plat-smt" and analysis == 'AliasAnalysis_C':
                    platsmt_alias_C.append(value)
                if tool_name == "plat-smt" and analysis == 'DataDepAnalysis':
                    platsmt_dd.append(value)

                j += 1
            fa.write('\n')
# ===================================  get speedup ===================================
    with open(f'./{analysis}_result.txt', 'a') as fb:
        speedup_yices = 0.0
        speedup_platsmt = 0.0
        if analysis == 'AliasAnalysis':
            for hh in range(alias_num):
                speedup_yices += graph_alias[hh]/yices_alias[hh]
                speedup_platsmt += graph_alias[hh]/platsmt_alias[hh]
            fb.write(f'speedup_yices={round(speedup_yices/alias_num, 2)}\n' )
            fb.write(f'speedup_platsmt={round(speedup_platsmt/alias_num, 2)}\n' )
        elif analysis == 'AliasAnalysis_C':
            for hh in range(alias_C_num):
                speedup_yices += graph_alias_C[hh]/yices_alias_C[hh]
                speedup_platsmt += graph_alias_C[hh]/platsmt_alias_C[hh]
            fb.write(f'speedup_yices={round(speedup_yices/alias_C_num, 2)}\n' )
            fb.write(f'speedup_platsmt={round(speedup_platsmt/alias_C_num, 2)}\n' )
        elif analysis == 'DataDepAnalysis':
            for hh in range(data_num):
                speedup_yices += graph_dd[hh]/yices_dd[hh]
                speedup_platsmt += graph_dd[hh]/platsmt_dd[hh]
            fb.write(f'speedup_yices={round(speedup_yices/data_num, 2)}\n' )
            fb.write(f'speedup_platsmt={round(speedup_platsmt/data_num, 2)}\n' )

# #============================================================== get query time  ================================================================
#
tools = [
    ('fastDyck',     '../../fastDyck_test/result/', False),
    ('Optimal',      '../../optimal_test/result/', False),
    ('z3',           '../../z3_test/result/',       False),
    ('cvc5',         '../../cvc5_test/result/',     False),
    ('Yices',        '../../Yices_test/result/',    False),
    ('platsmt',      '../../platsmt_test/result/',  True),
]

for analysis in analysis_Type:
    for tool_name, base_path, is_plat_smt in tools:
        if analysis == 'AliasAnalysis':
            benchmarks = AliasAnalysis
        elif analysis == 'AliasAnalysis_C':
            benchmarks = AliasAnalysis_C
        elif analysis == 'DataDepAnalysis':
            benchmarks = DataDep
        else:
            continue

        for bm in benchmarks:
            with open(f'./{analysis}_query/{bm}/{tool_name}.dat', 'w'):
                pass

        # 遍历 k=0~9
        for k in range(10):
            if analysis == 'AliasAnalysis':
                temp = [0.0] * alias_num
            elif analysis == 'AliasAnalysis_C':
                temp = [0.0] * alias_C_num
            elif analysis == 'DataDepAnalysis':
                temp = [0.0] * data_num

            for i in range(times):
                res_file = f'{base_path}{(k+1)*1000}/{analysis}{i}.res'
                try:
                    with open(res_file, 'r') as f:
                        pro_num = 0
                        record_start = 0.0
                        for line in f:
                            if is_plat_smt:
                                if "f_solved_time" in line:
                                    parts = line.split(":")
                                    record_start = int(parts[2])
                                if "query_time" in line:
                                    parts = line.split(":")
                                    current_time = int(parts[2])
                                    temp[pro_num] += (current_time - record_start) / 1000
                                    pro_num += 1
                            else:
                                if "query time" in line or "query_time" in line:
                                    find_time = find_floats(line)
                                    if find_time:
                                        temp[pro_num] += float(find_time[0])
                                        pro_num += 1
                except FileNotFoundError:
                    print(f"Warning: File not found: {res_file}")
                    continue

            num = 1
            for bm in benchmarks:
                file_path = f'./{analysis}_query/{bm}/{tool_name}.dat'
                with open(file_path, 'a') as fq:
                    if is_plat_smt:
                        if analysis == 'AliasAnalysis_C':
                            # Unit:seconds
                            value = round(temp[num - 1] / (1000 * times), 3)
                        else:
                            # Unit:milliseconds
                            value = round(temp[num - 1] / times, 3)
                    else:
                        if analysis == 'AliasAnalysis_C':
                            # Unit:seconds
                            value = round(temp[num - 1] / times, 3)
                        else:
                            # Unit:milliseconds
                            value = round(temp[num - 1] * 1000 / times, 3)
                    fq.write(f"{k + 1} {value}\n")
                num += 1
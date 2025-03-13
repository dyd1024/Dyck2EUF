import re

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

tool_type = [
    'z3',
    'cvc5',
    'Yices'
]

analysis_Type = [
    "AliasAnalysis",
    "DataDepAnalysis"
]

# fastDyck_alias = []
# optimal_alias = []
graph_alias = []
yices_alias = []
platsmt_alias=[]


yices_dd = []
platsmt_dd=[]
graph_dd = []

#============================================================== get analysis time  ================================================================

# FastDyck
for analysis in analysis_Type:
    with open(f'./{analysis}_result.txt', 'w') as f_temp:
        f_temp.write('')
    if analysis == 'AliasAnalysis':
        temp = [0.0]*11
    elif analysis == 'DataDepAnalysis':
        temp = [0.0]*15
    for i in range(3):
        with open(f'../../fastDyck_test/result/0/{analysis}{i}.res', 'r') as f:
            pro_num = 0
            for line in f:
                if "Time of graph constructed" in line:
                    find_time = find_floats(line)
                    temp[pro_num] = temp[pro_num] + float(find_time[0])
                    pro_num += 1

    with open(f'./{analysis}_result.txt', 'a') as fa:
        fa.write('FastDyck\n' )
        j=1
        for item in temp:
            fa.write(f'({j},{round(item*1000/3, 3)}) ')
            # if analysis == 'AliasAnalysis':
            #     graph_alias.append(item*1000/3)
            # elif analysis == 'DataDepAnalysis':
            #     graph_dd.append(item*1000/3)
            j+=1
        fa.write(f'\n' )

# Optimal
for analysis in analysis_Type:
    if analysis == 'AliasAnalysis':
        temp = [0.0]*11
    elif analysis == 'DataDepAnalysis':
        temp = [0.0]*15
    for i in range(3):
        with open(f'../../optimal_test/result/0/{analysis}{i}.res', 'r') as f:
            pro_num = 0
            for line in f:
                if "Time of graph constructed" in line:
                    find_time = find_floats(line)
                    temp[pro_num] = temp[pro_num] + float(find_time[0])
                    pro_num += 1

    with open(f'./{analysis}_result.txt', 'a') as fa:
        fa.write('Optimal\n' )
        j=1
        for item in temp:
            fa.write(f'({j},{round(item*1000/3, 3)}) ')
            if analysis == 'AliasAnalysis':
                graph_alias.append(item*1000/3)
            elif analysis == 'DataDepAnalysis':
                graph_dd.append(item*1000/3)
            j+=1
        fa.write(f'\n' )

# z3、cvc5、yices
for analysis in analysis_Type:
    for tool in tool_type:
        if analysis == 'AliasAnalysis':
            temp = [0.0] * 11
        elif analysis == 'DataDepAnalysis':
            temp = [0.0] * 15
        for i in range(3):
            with open(f'../../{tool}_test/result/0/{analysis}{i}.res', 'r') as f:
                pro_num = 0
                for line in f:
                    if "f_solved_time" in line:
                        find_time = find_floats(line)
                        temp[pro_num] = temp[pro_num] + float(find_time[0])
                        pro_num += 1

        with open(f'./{analysis}_result.txt', 'a') as fa:
            fa.write(f'{tool}\n')
            j = 1
            for item in temp:
                fa.write(f'({j},{round(item * 1000 / 3, 3)}) ')
                if tool == "Yices" and analysis == 'AliasAnalysis':
                    yices_alias.append(item * 1000 / 3)
                if tool == "Yices" and analysis == 'DataDepAnalysis':
                    yices_dd.append(item * 1000 / 3)
                j += 1
            fa.write(f'\n')

# plat-smt
for analysis in analysis_Type:
    if analysis == 'AliasAnalysis':
        temp = [0.0]*11
    elif analysis == 'DataDepAnalysis':
        temp = [0.0]*15
    for i in range(3):
        with open(f'../../platsmt_test/result/0/{analysis}{i}.res', 'r') as f:
            pro_num = 0
            record = 0.0
            for line in f:
                if ("start" in line) and not ( "startup" in line ):
                    find_time = line.split(":")
                    record = int(find_time[1])
                if "f_solved_time" in line:
                    find_time = line.split(":")
                    current_time = int(find_time[2])
                    temp[pro_num]=temp[pro_num] + (current_time-record)/1000
                    record = current_time
                    pro_num += 1

    with open(f'./{analysis}_result.txt', 'a') as fa:
        fa.write('platsmt\n' )
        j=1
        for item in temp:
            fa.write(f'({j},{round(item/3, 3)}) ')
            if analysis == 'AliasAnalysis':
                platsmt_alias.append(item/3)
            elif analysis == 'DataDepAnalysis':
                platsmt_dd.append(item/3)
            j+=1
        fa.write(f'\n' )

# ===================================  get speedup ===================================
#         speedup_yices = 0.0
#         speedup_platsmt = 0.0
#         if analysis == 'AliasAnalysis':
#             for hh in range(11):
#                 speedup_yices += graph_alias[hh]/yices_alias[hh]
#                 speedup_platsmt += graph_alias[hh]/platsmt_alias[hh]
#             fa.write(f'speedup_yices={round(speedup_yices/11, 2)}\n' )
#             fa.write(f'speedup_platsmt={round(speedup_platsmt/11, 2)}\n' )
#         elif analysis == 'DataDepAnalysis':
#             for hh in range(15):
#                 speedup_yices += graph_dd[hh]/yices_dd[hh]
#                 speedup_platsmt += graph_dd[hh]/platsmt_dd[hh]
#             fa.write(f'speedup_yices={round(speedup_yices/11, 2)}\n' )
#             fa.write(f'speedup_platsmt={round(speedup_platsmt/11, 2)}\n' )

#============================================================== get query time  ================================================================

# fastDyck
for analysis in analysis_Type:
    if analysis == 'AliasAnalysis':
        for bm in AliasAnalysis:
            with open(f'./{analysis}_query/{bm}/fastDyck.dat' , 'w') as fxx:
                fxx.write('')
    elif analysis == 'DataDepAnalysis':
       for bm in DataDep:
            with open(f'./{analysis}_query/{bm}/fastDyck.dat' , 'w') as fxx:
                fxx.write('')
    for k in range(10):
        if analysis == 'AliasAnalysis':
            temp = [0.0]*11
        elif analysis == 'DataDepAnalysis':
            temp = [0.0]*15
        for i in range(3):
            with open(f'../../fastDyck_test/result/{(k+1)*1000}/{analysis}{i}.res', 'r') as f:
                pro_num = 0
                for line in f:
                    if "query time" in line:
                        find_time = find_floats(line)
                        temp[pro_num] = temp[pro_num] + float(find_time[0])
                        pro_num += 1

        if analysis == 'AliasAnalysis':
            num=1
            for bm in AliasAnalysis:
                with open(f'./{analysis}_query/{bm}/fastDyck.dat' , 'a') as fq:
                    fq.write(f'{k+1} {round(temp[num-1]*1000/3, 3)}\n')
                num+=1
        if analysis == 'DataDepAnalysis':
            num=1
            for bm in DataDep:
                with open(f'./{analysis}_query/{bm}/fastDyck.dat' , 'a') as fq:
                    fq.write(f'{k+1} {round(temp[num-1]*1000/3, 3)}\n')
                num+=1

# optimal
for analysis in analysis_Type:
    if analysis == 'AliasAnalysis':
        for bm in AliasAnalysis:
            with open(f'./{analysis}_query/{bm}/Optimal.dat' , 'w') as fxx:
                fxx.write('')
    elif analysis == 'DataDepAnalysis':
       for bm in DataDep:
            with open(f'./{analysis}_query/{bm}/Optimal.dat' , 'w') as fxx:
                fxx.write('')
    for k in range(10):
        if analysis == 'AliasAnalysis':
            temp = [0.0]*11
        elif analysis == 'DataDepAnalysis':
            temp = [0.0]*15
        for i in range(3):
            with open(f'../../optimal_test/result/{(k+1)*1000}/{analysis}{i}.res', 'r') as f:
                pro_num = 0
                for line in f:
                    if "query time" in line:
                        find_time = find_floats(line)
                        temp[pro_num] = temp[pro_num] + float(find_time[0])
                        pro_num += 1

        if analysis == 'AliasAnalysis':
            num=1
            for bm in AliasAnalysis:
                with open(f'./{analysis}_query/{bm}/Optimal.dat' , 'a') as fq:
                    fq.write(f'{k+1} {round(temp[num-1]*1000/3, 3)}\n')
                num+=1
        if analysis == 'DataDepAnalysis':
            num=1
            for bm in DataDep:
                with open(f'./{analysis}_query/{bm}/Optimal.dat' , 'a') as fq:
                    fq.write(f'{k+1} {round(temp[num-1]*1000/3, 3)}\n')
                num+=1

# z3、cvc5、yices
for analysis in analysis_Type:
    for tool in tool_type:
        if analysis == 'AliasAnalysis':
            for bm in AliasAnalysis:
                with open(f'./{analysis}_query/{bm}/{tool}.dat' , 'w') as fxx:
                    fxx.write('')
        elif analysis == 'DataDepAnalysis':
            for bm in DataDep:
                with open(f'./{analysis}_query/{bm}/{tool}.dat' , 'w') as fxx:
                    fxx.write('')

        for k in range(10):
            if analysis == 'AliasAnalysis':
                temp = [0.0]*11
            elif analysis == 'DataDepAnalysis':
                temp = [0.0]*15
            for i in range(3):
                with open(f'../../{tool}_test/result/{(k+1)*1000}/{analysis}{i}.res', 'r') as f:
                    pro_num = 0
                    for line in f:
                        if "query_time" in line:
                            find_time = find_floats(line)
                            temp[pro_num] = temp[pro_num] + float(find_time[0])
                            pro_num += 1

            if analysis == 'AliasAnalysis':
                num=1
                for bm in AliasAnalysis:
                    with open(f'./{analysis}_query/{bm}/{tool}.dat' , 'a') as fq:
                        fq.write(f'{k+1} {round(temp[num-1]*1000/3, 3)}\n')
                    num+=1
            if analysis == 'DataDepAnalysis':
                num=1
                for bm in DataDep:
                    with open(f'./{analysis}_query/{bm}/{tool}.dat' , 'a') as fq:
                        fq.write(f'{k+1} {round(temp[num-1]*1000/3, 3)}\n')
                    num+=1

#
# plat-smt
for analysis in analysis_Type:
    if analysis == 'AliasAnalysis':
        for bm in AliasAnalysis:
            with open(f'./{analysis}_query/{bm}/platsmt.dat' , 'w') as fxx:
                fxx.write('')
    elif analysis == 'DataDepAnalysis':
        for bm in DataDep:
            with open(f'./{analysis}_query/{bm}/platsmt.dat' , 'w') as fxx:
                fxx.write('')
    for k in range(10):
        if analysis == 'AliasAnalysis':
            temp = [0.0]*11
        elif analysis == 'DataDepAnalysis':
            temp = [0.0]*15
        for i in range(3):
            with open(f'../../platsmt_test/result/{(k+1)*1000}/{analysis}{i}.res', 'r') as f:
                pro_num = 0
                record = 0.0
                for line in f:
                    if "f_solved_time" in line:
                        find_time = line.split(":")
                        record = int(find_time[2])
                    if "query_time" in line:
                        find_time = line.split(":")
                        current_time = int(find_time[2])
                        temp[pro_num]=temp[pro_num] + (current_time-record)/1000
                        record = current_time
                        pro_num += 1


        if analysis == 'AliasAnalysis':
            num=1
            for bm in AliasAnalysis:
                with open(f'./{analysis}_query/{bm}/platsmt.dat' , 'a') as fq:
                    fq.write(f'{k+1} {round(temp[num-1]/3, 3)}\n')
                num+=1
        if analysis == 'DataDepAnalysis':
            num=1
            for bm in DataDep:
                with open(f'./{analysis}_query/{bm}/platsmt.dat' , 'a') as fq:
                    fq.write(f'{k+1} {round(temp[num-1]/3, 3)}\n')
                num+=1

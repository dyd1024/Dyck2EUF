import subprocess

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

tool_type=[
    "optimal",
    "fastDyck",
    "plat-smt",
    "yices",
    "z3",
    "cvc5"
]

analysis_Type = [
    "AliasAnalysis",
    "DataDepAnalysis"
]
times = 3

for analysisType in analysis_Type:
    if analysisType == "AliasAnalysis":
        benchmarks = AliasAnalysis
    elif analysisType == "DataDepAnalysis":
        benchmarks = DataDep

    for j in range(11):
        for i in range(times):
            with open(f'../cvc5_test/result/{j*1000}/{analysisType}{i}.res','w') as outfile:
                for bm in benchmarks:
                    subprocess.run(
                        ['../cvc5_test/cvc5',f'./smt2_{analysisType}/{j*1000}/{bm}.smt2', '--incremental'],
                        stdout=outfile,
                        stderr=subprocess.STDOUT
                    )
    for j in range(11):
        for i in range(times):
            with open(f'../platsmt_test/result/{j*1000}/{analysisType}{i}.res','w') as outfile:
                for bm in benchmarks:
                    subprocess.run(
                        ['../platsmt_test/plat-smt',f'./smt2_{analysisType}/{j*1000}/{bm}.smt2'],
                        stdout=outfile,
                        stderr=subprocess.STDOUT
                    )
    for j in range(11):
        for i in range(times):
            with open(f'../Yices_test/result/{j*1000}/{analysisType}{i}.res','w') as outfile:
                for bm in benchmarks:
                    subprocess.run(
                        ['../Yices_test/yices-smt2',f'./smt2_{analysisType}/{j*1000}/{bm}.smt2','--incremental'],
                        stdout=outfile,
                        stderr=subprocess.STDOUT
                    )
    for j in range(11):
        for i in range(times):
            with open(f'../z3_test/result/{j*1000}/{analysisType}{i}.res','w') as outfile:
                for bm in benchmarks:
                    subprocess.run(
                        ['../z3_test/z3',f'./smt2_{analysisType}/{j*1000}/{bm}.smt2'],
                        stdout=outfile,
                        stderr=subprocess.STDOUT
                    )
    for j in range(11):
        for i in range(times):
            with open(f'../optimal_test/result/{j*1000}/{analysisType}{i}.res','w') as outfile:
                for bm in benchmarks:
                    subprocess.run(
                        ['../optimal_test/optimal',f'./SPG_{analysisType}/0/{bm}.spg',f'./SPG_{analysisType}/{j*1000}/{bm}.seq'],
                        stdout=outfile,
                        stderr=subprocess.STDOUT
                    )
    for j in range(11):
        for i in range(times):
            with open(f'../fastDyck_test/result/{j*1000}/{analysisType}{i}.res','w') as outfile:
                for bm in benchmarks:
                    subprocess.run(
                        ['../fastDyck_test/fastDyck',f'./SPG_{analysisType}/0/{bm}.spg',f'./SPG_{analysisType}/{j*1000}/{bm}.seq'],
                        stdout=outfile,
                        stderr=subprocess.STDOUT
                    )

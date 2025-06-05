import os
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

AliasAnalysis=[
    'antlr', 'bloat', 'chart', 'eclipse', 'fop', 'hsqldb', 'jython', 'luindex', 'lusearch', 'pmd', 'xalan'
]

AliasAnalysis_C=[
    'git', 'libssh2.a', 'tmux', 'vim', 'lighttpd', 'sqlite3', 'strace', 'wrk', 'darknet', 'libxml2.a'
]

DataDep = [
    'btree', 'check', 'compiler', 'compress', 'crypto', 'derby', 'helloworld', 'mpegaudio', 'mushroom', 'parser', 'sample', 'scimark', 'startup', 'sunflow', 'xml'
]

# config information
tool_config = {
    "optimal": {
        "path": "../optimal_test/optimal",
        "args": lambda j, bm: [f"./Input/SPG_{analysisType}/0/{bm}.spg", f"./Input/SPG_{analysisType}/{j}/{bm}.seq"]
    },
    "fastDyck": {
        "path": "../fastDyck_test/fastDyck",
        "args": lambda j, bm: [f"./Input/SPG_{analysisType}/0/{bm}.spg", f"./Input/SPG_{analysisType}/{j}/{bm}.seq"]
    },
    "platsmt": {
        "path": "../platsmt_test/plat-smt",
        "args": lambda j, bm: [f"./Input/smt2_{analysisType}/{j}/{bm}.smt2"]
    },
    "Yices": {
        "path": "../Yices_test/yices-smt2",
        "args": lambda j, bm: [f"./Input/smt2_{analysisType}/{j}/{bm}.smt2", "--incremental"]
    },
    "z3": {
        "path": "../z3_test/z3",
        "args": lambda j, bm: [f"./Input/smt2_{analysisType}/{j}/{bm}.smt2"]
    },
    "cvc5": {
        "path": "../cvc5_test/cvc5",
        "args": lambda j, bm: [f"./Input/smt2_{analysisType}/{j}/{bm}.smt2", "--incremental"]
    }
}

analysis_Type = [
    "AliasAnalysis",
    "AliasAnalysis_C",
    "DataDepAnalysis"
]
times = 3

def run_benchmark(tool_name, benchmarks, analysisType, j, i):
    tool_info = tool_config[tool_name]
    output_dir = f"../{tool_name}_test/result/{j}"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/{analysisType}{i}.res"

    with open(output_file, 'w') as outfile:
        for bm in benchmarks:
            cmd = [tool_info["path"]] + tool_info["args"](j, bm)
            print(f"Running command: {' '.join(cmd)}"+'\n')
            subprocess.run(
                cmd,
                stdout=outfile,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=600  # timeout 600s
            )
            outfile.flush()
            os.fsync(outfile.fileno())
    # return bm, result.returncode

def parallel_run(tool_name, benchmarks, analysisType, j_values, times):
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = []
        for j in j_values:
            for i in range(times):
                futures.append(executor.submit(run_benchmark, tool_name, benchmarks, analysisType, j*1000, i))

        # for future in as_completed(futures):
        #     bm, code = future.result()
        #     print(f"[{tool_name}] Benchmark {bm} finished with return code {code}")

if __name__ == "__main__":
    j_values = list(range(11))  # j from 0 to 10

    start_time = time.time()

    for analysisType in analysis_Type:
        if analysisType == "AliasAnalysis":
            benchmarks = AliasAnalysis
        elif analysisType == "DataDepAnalysis":
            benchmarks = DataDep
        elif analysisType == "AliasAnalysis_C":
            benchmarks = AliasAnalysis_C

        for tool_name in tool_config:
            print(f"\nRunning benchmark for tool: {tool_name}, analysis type: {analysisType}")
            parallel_run(tool_name, benchmarks, analysisType, j_values, times)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Timecost: {elapsed_time:.2f} s")
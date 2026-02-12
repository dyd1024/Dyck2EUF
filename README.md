# Dyck2EUF
This is the artifact for the submission titled **EUF-based Solving Dyck-Reachability with Applications to Static Analysis**.

# Prerequisites
+ Unix / Linux OS: We have validated the artifact on Ubuntu 22.04 system
+ Python3 >= 3.8
+ Java >= 1.8


# Project directory structure description
```text
Dyck2EUF/
├── benchmark/                  # Benchmarking & experimental data
│   ├── C_program/              # Real-world C programs used in experiments
│   │   ├── programs/           # Compiled LLVM bitcode files (.bc)
│   │   ├── dumpDyckGraph       # C-to-DOT graph encoder
│   │   └── runDyckAA.py        # Script to generate Dyck graph from C code
│   ├── datalog_result/         # Output results from Datalog solvers
│   ├── Dot/                    # DOT files representing program graphs
│   ├── Input/                  # Input files in various formats for different tools
│       ├── gen_union.py        #
│       ├── trans.py            # Converts DOT files into input formats for graph/SMT tools
│       └── trans_datalog.py    # Converts DOT files into input format for Datalog tools
│   ├── libbuddy.so             # Java BDD library required by bddbddb
│   ├── run.py                  # Main script for running graph- and SMT-based tools
│   ├── run_datalog_seq.py      # Script for running Datalog tools
│   └── total_result            # Results from graph- and SMT-based analysis tools
│       ├── *_query/            # The results of each tool on the query experiment
│       ├── *_result.txt        # The results of each tool on the solving experiment
│       ├── check.py            # Check if the results of each tool are consistent
│       └── get_result.py       # Results summary script
├── *_test/                     # Tool-specific directories (e.g., z3_test, optimal_test)
│   ├── result/                 # Execution results for the corresponding tool
│   └── example.*               # Example programs for testing the tool
├── .gitignore                  # Git ignore rules
├── check_tools.py              # Check if all tools are functioning properly
└── README.md                   # Project overview and usage instructions
```


# Running the artifact
We assume that the following commands are run in sudo mode.

**Smoke Test.** Before conducting experiments, run the following script to check if all tools function properly in the current environment. (This step can be completed in around 1 second.)

```sh
cd /Dyck2EUF/
python3 check_tools.py
```

**Reproducing the Experimental Results of Graph-based and EUF SMT-based Tools.**
First, we need to generate a total of 10 query sequences for each program in the three benchmarks, with lengths varying from 1,000 to 10,000 in increments of 1,000. You have the option to regenerate these sequences or use the existing data. To regenerate the query sequences, please run the following code (this step takes approximately 45 minutes to complete on my machine):


```sh
cd /Dyck2EUF/benchmark/Input/
python3 trans.py
```

Next, run the graph-based methods FastDyck and Optimal, as well as the EUF SMT solver tools, on the benchmark using the following command (we have commented out egg due to its prohibitively long runtime; uncomment if needed):

```sh
cd /Dyck2EUF/benchmark/
python3 run.py
```
Run the following command to verify that the query results from the EUF SMT solver methods are consistent with those from the graph-based methods (this step takes approximately 10s to complete on my machine).

```sh
cd /Dyck2EUF/benchmark/total_result/
python3 check.py
```

Run the following command to conduct a statistical analysis of the experimental results. The experimental results are located in **/benchmark/total_result/**, where **AliasAnalysis_result.txt**, **AliasAnalysis_C_result.txt**, and **DataDepAnalysis_result.txt** contain the results of alias analysis for Java programs, alias analysis for C programs, and data dependence analysis, respectively. The query experimental results can be found in the **AliasAnalysis_query**, **AliasAnalysis_C_query** and **DataDepAnalysis_query** folders, saved in **.dat** format (all results represent the average of three runs):

```sh
cd /Dyck2EUF/benchmark/total_result/
python3 get_result.py
```

**Reproducing the Experimental Results of the Datalog Tools.**
Run the following command to generate a query sequence with a length of 1,000 for each program (this step takes approximately 70s to complete on my machine):

```sh
cd /Dyck2EUF/benchmark/
python3 trans_datalog.py
```

Run the following command to evaluate the performance of the Datalog tools **Bddbddb** and **Soufflé** on these two benchmarks (this step takes approximately 22 hours to complete on my machine):

```sh
cd /Dyck2EUF/benchmark/
python3 run_datalog_seq.py
```
The results of the runs are located in the folder **/benchmark/datalog_result**. The runtime statistics can be found in **result.txt**, which contains the averages from three runs.

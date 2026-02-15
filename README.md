# Dyck2EUF
This is the artifact for the submission titled **EUF-based Solving Dyck-Reachability with Applications to Static Analysis**.


## Introduction

- **Abstract.** Dyck-reachability offers a fundamental formulation for static analysis by modeling critical properties like field and context sensitivity through Dyck grammars. This paper presents a novel encoding of Dyck-reachability problems on bidirected graphs into Equality with Uninterpreted Functions (EUF) SMT problems. This connection, introduced here for the first time, enables a method that directly leverages SMT solvers to perform static analysis tasks, reducing the need for dedicated algorithm development while maintaining competitive efficiency.
This artifact reproduces all experiments presented in the paper. It includes performance evaluations of graph-based, SMT-solver-based, and Datalog-based tools for conducting field-sensitive alias analysis on Java and C programs, as well as context-sensitive data-dependence analysis on Java programs. Furthermore, the artifact compares the efficiency of union-find operations across different language implementations and algorithmic variants.

- **Purepose.** This This artifact aims to evaluate the following two research questions:
    - _**RQ1**: Efficiency of analysis, i.e., given a program and a static analysis task, how efficient is the SMT solver-based approach compare to the other two approachs in completing the analysis?_
    - _**RQ2**: Efficiency of querying, *i.e.*, after completing alias analysis, how efficient is SMT solver-based approach compare to the other two approachs in querying whether any two variables are aliases?_

- **Claims.** The tools to be compared include graph-based tools Optimal and FD; SMT solvers Z3, CVC5, Yices, Plat-smt, and Egg; and Datalog tools Soufflé and BddBddb.

## Prerequisites
To use this artifact, you only need a system capable of running **Docker**.

- **Operating System**: Linux (tested on Ubuntu 22.04); macOS or Windows with Docker Desktop also supported
- **Docker Engine**: version 20.10 or higher
- **Hardware**:
  - CPU: x86_64 architecture (Intel/AMD), 4 cores or more recommended
  - Memory: at least **4 GB RAM**
  - Disk Space: **~8 GB free space** (for the Docker image and temporary files)


## Step-by-Step Reproduction Guide
We provide a Docker image to help you reproduce the results: `dyck2euf.tar.gz`. Please download it and run the container using the commands below.

```sh
# Load the compressed image into Docker
gunzip -c dyck2euf.tar.gz | docker load

# Verify that the image has been loaded successfully
docker images | grep dyck2euf

# Run the Docker container
docker run --rm -it dyck2euf bash
```

- **Smoke Test.**  Before conducting experiments, verify that all tools work correctly using the provided Docker image. This ensures a consistent and reproducible environment. (~1s)

    ```sh
    python3 check_tools.py
    ```
    The command executes an example program for each tool. Graph-based tools report file parsing time, solving time, total time, query results (**Reachability** or **not Reachability**), and query time. SMT-based tools provide similar output, with query results categorized as **sat** or **unsat**. For the Datalog tool BddBddb, queries are resolved by checking set size—for instance, "SIZE OF q: 1" indicates a non-empty query set, meaning the two nodes are equivalent. Soufflé outputs results in CSV files, viewable under **souffle_test/**. If all nine tools pass the test, the smoke test is considered successful.


- **Reproducing the Experimental Results of Graph-based and EUF SMT-based Tools. (see Tables 4-6 and Appendix Figures 5-7)**
   - **Random Query Sequence Generation (Optional, ~1.5h)**
 Our benchmark already includes randomly generated query sequences, so this step can be skipped. If you wish to regenerate them, run the following command:

        ```sh
        cd /app/benchmark/Input/ && python3 trans.py
        ```
        This command will generate 10 query sequences for each program in the three benchmarks, with lengths ranging from 1,000 to 10,000 in increments of 1,000.

  - **Replicating Experimental Results for Alias Analysis in Java Programs (see Table 4 and Appendix Figure 5; time: ~12 min)**
    Run the following command to perform field-sensitive alias analysis for Java programs using graph-based and SMT-solver tools. The experiment covers both solving and querying across sequences of lengths 1,000 to 10,000, with results averaged over three runs.

    ```sh
    cd /app/benchmark/ && python3 run_Java_alias.py
    ```
    Run the following command to view the solving experiment results, which address **RQ1** (Table 4, showing averages over three runs).

    ```sh
    cd /app/benchmark/total_result/ && cat AliasAnalysis_result.txt
    ```
    In the results, each tool's data comprises 11 rows, each representing the total time (file parsing + solving) for that tool on a different program.
    For query experiment results (Figure 5), which address **RQ2**, run the command **cd benchmark/total_result/AliasAnalysis_query && ls**. The folders named after each program contain the query results for that program. For example, proceed with **cd antlr/ && ls** to see the query times of different tools for antlr. Then, run **cat cvc5.dat** to view the data: 10 lines represent the average query time (in ms, over three runs) of cvc5 on antlr across the 10 query sequences of lengths 1,000 to 10,000 (step size: 1,000).

  - **Replicating Experimental Results for Alias Analysis in C Programs (see Table 5 and Appendix Figure 6; time: ~5h)**
    Similar to the experiment above, run the following command to perform field-sensitive alias analysis for Java programs using graph-based and SMT-solver tools. The execution also includes both solving and querying experiments：
    ```sh
    cd /app/benchmark/ && python3 run_C_alias.py
    ```
    Run the following command to view the solving experiment results, which address **RQ1** (Table 5, showing averages over three runs):
    ```sh
    cd /app/benchmark/total_result/ && cat AliasAnalysis_C_result.txt
    ```
    The results of the query experiments are located in the directory **benchmark/total_result/AliasAnalysis_C_query**. These results address **RQ2**​ and follow the same structure as the previous experiment.

  - **Replicating Experimental Results for Context-sensitive Data Dependence Analysis on​ Java Programs (see Table 6 and Appendix Figure 7; time: ~6min)**
  Run the following command to perform context-sensitive data dependence analysis on Java programs using graph-based and SMT-solver tools. The analysis includes both solving and querying experiments.
    ```sh
    cd /app/benchmark/ && python3 run_Java_dd.py
    ```
    Run the following command to view the solving experiment results, which address **RQ1** (Table 6, showing averages over three runs):
    ```sh
    cd /app/benchmark/total_result/ && cat DataDepAnalysis_result.txt
    ```
    The results of the query experiments are located in the directory **benchmark/total_result/DataDepAnalysis_query**. These results address **RQ2**​ and follow the same structure as the previous experiment.

  - **Cross-Tool Result Consistency Check.**
  Run the following command to verify that the query results from the EUF SMT solver methods are consistent with those from the graph-based methods (~10s).

      ```sh
      cd /app/benchmark/total_result/ && python3 check.py
      ```

- **Replicating Experiments on Union-Find Operations Across Different Tools (see Table 10 in Appendix, time:~1min)**
Run the following command to generate Union-Find sequences with lengths ranging from 5,000 to 25,000 (step size: 5,000). (Optional, ~1 s)
    ```sh
    cd /app/benchmark/Input/ && python3 trans.py
    ```
    Run the following command to test the performance of different tools on the Union-Find sequences generated above.
    ```sh
    cd /app/benchmark/ && python3 run_Union_Find.py
    ```
    Run the following command to view the experiment results (Table 10, showing averages over three runs):
    ```sh
    cd /app/benchmark/total_result/ && cat unionfind_result.txt
    ```

- **Reproducing the Experimental Results of the Datalog Tools (see Tables 7-9 in Appendix, time:~25h).**
Run the following command to generate a query sequence with a length of 1,000 for each program (Optional, ~90s):

    ```sh
    cd /app/benchmark/Input/ && python3 trans_datalog.py
    ```

    Run the following command to evaluate the performance of the Datalog tools **Bddbddb** and **Soufflé** on these three benchmarks (~25h):

    ```sh
    cd /app/benchmark/ && python3 run_datalog_seq.py
    ```
    Execute the following command to view the average runtime results (over three runs) for the two Datalog tools, as presented in Tables 7-9.

    ```sh
    cd /app/benchmark/datalog_result/ && cat result.txt
    ```

    The execution results for each Datalog tool on every program using query sequences of length 1,000 can be found in the bddbddb and souffle directories under **/benchmark/datalog_result**.
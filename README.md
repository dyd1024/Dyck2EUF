# Dyck2EUF
This is the artifact for the submission titled **SMT-based Solving of Dyck-Reachability with Applications to Static Analysis**.

# Prerequisites
+ Unix / Linux OS: We have validated the artifact on Ubuntu 22.04 system
+ Python3 >= 3.8
+ Java >= 1.8

# Running the artifact
We assume that the following commands are run in sudo mode.

**Ensure that each tool functions correctly.** Before conducting experiments, run each tool individually to verify that they can successfully execute in the current environment, using the following commands for testing.

`FastDyck`

```sh
cd /Dyck2EUF/fastDyck_test/
./fastDyck example.spg example.seq
```

`Optimal`

```sh
cd /Dyck2EUF/optimal_test/
./optimal example.spg example.seq
```

`CVC5`

```sh
cd /Dyck2EUF/cvc5_test/
./cvc5 example.smt2 --incremental
```

`Z3`

```sh
cd /Dyck2EUF/z3_test/
./z3 example.smt2
```

`Yices`

```sh
cd /Dyck2EUF/Yices_test/
./yices-smt2 example.smt2 --incremental
```

`Plat-smt`

```sh
cd /Dyck2EUF/platsmt_test/
./plat-smt example.smt2
```

`Bddbddb`

```sh
cd /Dyck2EUF/bddbddb_test/
java -jar bddbddb-full.jar example.datalog
```

`Soufflé`

```sh
cd /Dyck2EUF/souffle_test/
./souffle example.dl
```
**Reproducing the experimental results.**
First, we need to generate a total of 10 query sequences for each program, with lengths varying from 1,000 to 10,000 in increments of 1,000. You have the option to regenerate these sequences or use the existing data. To regenerate the query sequences, please run the following code (this step takes approximately 6 minutes to complete on my machine):


```sh
cd /Dyck2EUF/benchmark/
python3 trans.py
```

Next, run the graph-based methods FastDyck and Optimal, as well as the EUF SMT solver tools, including Z3, CVC5, Yices, and Plat-smt, on the benchmark using the following command (this step takes approximately 15 minutes to complete on my machine):

```sh
cd /Dyck2EUF/benchmark/
python3 run.py
```
Run the following command to verify that the query results from the EUF SMT solver methods are consistent with those from the graph-based methods.

```sh
cd /Dyck2EUF/benchmark/total_result/
python3 check.py
```

Run the following command to conduct a statistical analysis of the experimental results. The results from **Section 4.2** are located in **/benchmark/total_result/**, where **AliasAnalysis_result.txt** and **DataDepAnalysis_result.txt** contain the results of alias analysis and data dependence analysis, respectively. The experimental results from **Section 4.3** can be found in the **AliasAnalysis_query** and **DataDepAnalysis_result** folders, saved in **.dat** format (all results represent the average of three runs):

```sh
cd /Dyck2EUF/benchmark/total_result/
python3 get_result.py
```

**Reproducing the experimental results of the Datalog tools.**
Run the following command to generate a query sequence with a length of 1,000 for each program:

```sh
cd /Dyck2EUF/benchmark/
python3 trans_datalog.py
```

Run the following command to evaluate the performance of the Datalog tools **Bddbddb** and **Soufflé** on these two benchmarks (this step takes approximately 7 hours to complete on my machine):

```sh
cd /Dyck2EUF/benchmark/
python3 run_datalog_seq.py
```
The results of the runs are located in the folder **/benchmark/datalog_result**. The runtime statistics can be found in **result.txt**, which contains the averages from three runs.

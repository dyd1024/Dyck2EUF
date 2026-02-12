#!/usr/bin/env python3
import os
import subprocess
import sys

# Define test tasks: each item is a tuple (working_directory, command_as_list)
tasks = [
    ("./fastDyck_test/", ["./fastDyck", "example.spg", "example.seq"]),
    ("./optimal_test/", ["./optimal", "example.spg", "example.seq"]),
    ("./cvc5_test/", ["./cvc5", "example.smt2", "--incremental"]),
    ("./z3_test/", ["./z3", "example.smt2"]),
    ("./Yices_test/", ["./yices-smt2", "example.smt2", "--incremental"]),
    ("./platsmt_test/", ["./plat-smt", "example.smt2"]),
    ("./bddbddb_test/", ["java", "-jar", "bddbddb-full.jar", "example.datalog"]),
    ("./souffle_test/", ["./souffle", "example.dl"]),
    ("./egg_R_test/", ["./egg_R", "example.smt2"])
]

def run_task(workdir, cmd):
    try:
        # Check if the working directory exists
        if not os.path.isdir(workdir):
            print(f"[ERROR] Directory does not exist: {workdir}")
            return False

        # For commands starting with './', verify the executable file exists
        if cmd[0].startswith("./"):
            exe_path = os.path.join(workdir, cmd[0][2:])  # Remove './'
            if not os.path.isfile(exe_path):
                print(f"[ERROR] Executable not found: {exe_path}")
                return False

        print(f"Running: cd {workdir} && {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=workdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300  # Timeout after 5 minutes to avoid hanging
        )

        if result.returncode == 0:
            print(f"[SUCCESS] Command executed successfully: {' '.join(cmd)}\n")
            return True
        else:
            print(f"[FAILURE] Command failed: {' '.join(cmd)}")
            print(f"  Return code: {result.returncode}")
            if result.stderr.strip():
                print(f"  Error output:\n{result.stderr}")
            if result.stdout.strip():
                print(f"  Standard output:\n{result.stdout}")
            print()
            return False

    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] Command timed out: {' '.join(cmd)}\n")
        return False
    except FileNotFoundError as e:
        print(f"[ERROR] Command or file not found: {e}\n")
        return False
    except Exception as e:
        print(f"[EXCEPTION] An unexpected error occurred: {e}\n")
        return False

def main():
    print("Starting tool execution checks...\n")
    success_count = 0
    total_count = len(tasks)

    for workdir, cmd in tasks:
        if run_task(workdir, cmd):
            success_count += 1

    print(f"Check completed! Success: {success_count}/{total_count}")
    if success_count != total_count:
        sys.exit(1)  # Exit with error code if any task failed

if __name__ == "__main__":
    main()

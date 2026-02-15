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

        tool_name = cmd[0][2:] if cmd[0].startswith("./") else cmd[0]
        full_cmd_str = ' '.join(cmd)
        print(f"\n{'='*60}")
        print(f"Testing {tool_name}: cd {workdir} && {full_cmd_str}")
        print(f"{'-'*60}")

        result = subprocess.run(
            cmd,
            cwd=workdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=600  # Timeout after 5 minutes
        )

        # Always print stdout and stderr (even if empty)
        if result.stdout.strip():
            print("STDOUT:")
            print(result.stdout)
        else:
            print("STDOUT: <empty>")

        if result.stderr.strip():
            print("STDERR:")
            print(result.stderr)
        else:
            print("STDERR: <empty>")

        if result.returncode == 0:
            print(f"[SUCCESS] Command succeeded: {full_cmd_str}")
            return True
        else:
            print(f"[FAILURE] Command failed (return code {result.returncode}): {full_cmd_str}")
            return False

    except subprocess.TimeoutExpired as e:
        print(f"[TIMEOUT] Command timed out after 300 seconds: {' '.join(cmd)}")
        if e.stdout:
            print("STDOUT (partial):")
            print(e.stdout.decode() if isinstance(e.stdout, bytes) else e.stdout)
        if e.stderr:
            print("STDERR (partial):")
            print(e.stderr.decode() if isinstance(e.stderr, bytes) else e.stderr)
        return False

    except FileNotFoundError as e:
        print(f"[ERROR] Command or file not found: {e}")
        return False

    except Exception as e:
        print(f"[EXCEPTION] An unexpected error occurred: {e}")
        return False

def main():
    print("Starting tool execution checks...\n")
    success_count = 0
    total_count = len(tasks)

    for workdir, cmd in tasks:
        if run_task(workdir, cmd):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"Check completed! Success: {success_count}/{total_count}")
    if success_count != total_count:
        sys.exit(1)  # Exit with error code if any task failed

if __name__ == "__main__":
    main()

import os
import subprocess
from multiprocessing import Pool, cpu_count
import time

input_dir = 'Dyck_programs'
output_dir = '../Dot/AliasAnalysis_C'

os.makedirs(output_dir, exist_ok=True)

dyck = "./dumpDyckGraph"

bc_files = [f for f in os.listdir(input_dir) if f.endswith('.bc')]

def run_dump(file):
    input_path = os.path.join(input_dir, file)
    output_name = os.path.splitext(file)[0] + '.dot'
    output_path = os.path.join(output_dir, output_name)
    cmd = [dyck, input_path, '--output-file=' + output_path]
    try:
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {file}: {e}")

# parallel version
# if __name__ == '__main__':
#     start_time = time.time()
#     with Pool(processes=cpu_count()) as pool:
#         pool.map(run_dump, bc_files)
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"Timecost: {elapsed_time:.2f} ss")

# serial version
if __name__ == '__main__':
    start_time = time.time()

    for file in bc_files:
        run_dump(file)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Timecost: {elapsed_time:.2f} s")


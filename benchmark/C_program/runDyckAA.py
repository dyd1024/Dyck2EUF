import os
import subprocess
from multiprocessing import Pool, cpu_count

input_dir = 'programs'
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

if __name__ == '__main__':
    with Pool(processes=cpu_count()) as pool:
        pool.map(run_dump, bc_files)



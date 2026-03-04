import os
from pathlib import Path
from collections import defaultdict

def calculate_averages(top_directory):
    """
    计算指定目录下所有子文件夹中相同.dat文件的平均值

    参数:
        top_directory: 顶层目录路径 (包含 AliasAnalysis_C_query, AliasAnalysis_query, DataDepAnalysis_query)
    """

    # 获取顶层目录下的三个主文件夹
    main_folders = [
        'AliasAnalysis_C_query',
        'AliasAnalysis_query',
        'DataDepAnalysis_query'
    ]

    for main_folder in main_folders:
        main_path = Path(top_directory) / main_folder

        if not main_path.exists():
            print(f"警告: 文件夹 {main_folder} 不存在")
            continue

        print(f"\n处理文件夹: {main_folder}")

        # 获取该主文件夹下的所有子文件夹
        sub_folders = [f for f in main_path.iterdir() if f.is_dir()]

        if not sub_folders:
            print(f"  没有找到子文件夹")
            continue

        print(f"  找到 {len(sub_folders)} 个子文件夹")

        # 用于存储每个.dat文件的所有数据
        dat_files_data = defaultdict(lambda: defaultdict(list))

        # 遍历所有子文件夹，读取.dat文件
        for sub_folder in sub_folders:
            print(f"    处理子文件夹: {sub_folder.name}")

            # 获取子文件夹中的所有.dat文件
            dat_files = list(sub_folder.glob('*.dat'))

            for dat_file in dat_files:
                filename = dat_file.name

                try:
                    with open(dat_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    # 解析每一行的数据
                    for line_num, line in enumerate(lines):
                        line = line.strip()
                        if line:  # 跳过空行
                            try:
                                # 假设格式为 "序号 数值"，我们只需要数值部分
                                parts = line.split()
                                if len(parts) >= 2:
                                    value = float(parts[1])  # 取第二个部分作为数值
                                    dat_files_data[filename][line_num].append(value)
                                elif len(parts) == 1:
                                    # 如果只有一部分，直接作为数值
                                    value = float(parts[0])
                                    dat_files_data[filename][line_num].append(value)
                            except ValueError:
                                print(f"      警告: 无法解析 {dat_file.name} 第 {line_num + 1} 行: {line}")

                except Exception as e:
                    print(f"      错误: 读取文件 {dat_file} 时出错: {e}")

        # 计算平均值并写入文件
        for filename, line_data in dat_files_data.items():
            output_path = main_path / filename

            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    # 按行号排序，确保顺序正确
                    sorted_lines = sorted(line_data.items())

                    for line_num, values in sorted_lines:
                        if values:  # 确保有数据
                            average = sum(values) / len(values)
                            # 写入格式: "序号 平均值"
                            f.write(f"{line_num + 1} {average:.6f}\n")

                print(f"  已生成平均值文件: {filename}")

            except Exception as e:
                print(f"  错误: 写入文件 {output_path} 时出错: {e}")

def main():
    # 设置顶层目录路径
    # 请根据你的实际路径修改这里
    top_directory = r'C:\Users\Lenovo\Desktop\temp\dat'  # 修改为你的实际路径

    # 或者使用相对路径（如果脚本在正确的位置）
    # top_directory = '.'

    print("开始处理.dat文件...")
    print(f"顶层目录: {top_directory}")

    calculate_averages(top_directory)

    print("\n处理完成!")

if __name__ == "__main__":
    main()
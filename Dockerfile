# 使用 Ubuntu 22.04（jammy）作为基础镜像
FROM ubuntu:22.04

# 设置非交互式安装（避免 tzdata 弹窗）
ENV DEBIAN_FRONTEND=noninteractive

# 安装 Python 3.10、OpenJDK 8、unzip 和其他工具
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        openjdk-8-jre \
        unzip \
        && \
    rm -rf /var/lib/apt/lists/*

# 设置 JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 赋予所有工具可执行权限
RUN chmod +x ./fastDyck_test/fastDyck \
    && chmod +x ./optimal_test/optimal \
    && chmod +x ./cvc5_test/cvc5 \
    && chmod +x ./z3_test/z3 \
    && chmod +x ./Yices_test/yices-smt2 \
    && chmod +x ./platsmt_test/plat-smt \
    && chmod +x ./souffle_test/souffle \
    && chmod +x ./egg_R_test/egg_R \
    && chmod +x ./benchmark/Input/get_result

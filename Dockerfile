# 使用基础镜像
FROM dockerproxy.cn/cnstark/pytorch:1.12.1-py3.9.12-cuda11.6.2-devel-ubuntu20.04

# 设置工作目录
WORKDIR /submit

# 将当前目录的所有内容复制到容器内的 /submit 目录
COPY . /submit

# 确保使用国内的 pip 源进行依赖安装
RUN pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# # 卸载当前 Python 版本
# RUN apt-get update && \
#     apt-get remove -y python3 python3-pip && \
#     apt-get autoremove -y

# # 安装 Python 3.10
# RUN apt-get update && \
#     apt-get install -y software-properties-common && \
#     add-apt-repository -y ppa:deadsnakes/ppa && \
#     apt-get update && \
#     apt-get install -y python3.10 python3.10-venv python3.10-distutils && \
#     curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

# # 将 python 和 pip 的默认指向更新到 Python 3.10
# RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 && \
#     update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip 1

# 确保 install.sh 可执行
RUN chmod +x /submit/install.sh

# 运行 install.sh 脚本，安装项目依赖
RUN /submit/install.sh

# 创建output文件夹
RUN mkdir /output

# 设置默认命令，进入工作目录并启动交互式 shell（可根据需求调整）
CMD ["bash"]

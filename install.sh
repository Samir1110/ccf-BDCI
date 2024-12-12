#!/bin/bash
cd 620ccf


##### 安装依赖
pip install -e '.[torch,metrics]' --index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
pip install antlr4-python3-runtime --index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
pip install modelscope --index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
pip install tyro==0.8.14 --index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

##### 返回上级目录
cd ..

python download.py

echo "Setup completed successfully!"

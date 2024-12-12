#!/bin/bash
######### 1、将原始的test输入格式转换成模型预测格式，运行test_change.py
python ./620ccf/test_change.py 

######### 2、运行测试代码
bash ./620ccf/test_exp.sh
## --model_name_or_path
## --adapter_name_or_path
## 需要重新确认上述路径

######## 3、重复纠错
python ./620ccf/GrammarCheck/GrammarCheckMulti.py
# 需要重新修改其中用到的test_correct.sh中的
# --model_name_or_path
# --adapter_name_or_path

######## 4、得到最终的生成语言，运行：LLaMA-Factory/lib/change/result.py
python ./620ccf/result.py
#line6需要修改一下路径
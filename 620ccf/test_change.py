################ 把测试数据集修改成预测所需的格式

import json

# 读取原始JSON数据
with open('../test_cypher.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 遍历每一条记录，生成output
for item in data:
    question = item.get('question', '')
    
# 构造包含instruction字段的完整数据
output_data = []
for item in data:
    output_data.append({
        "instruction": "你是一个TuGraph翻译机器,根据以下输入问题(input),你应该生成对应的Cypher查询语句(output)。请确保你输出的结果必须只包含正确的Cypher查询语句,不要包含任何推测、注释或多余的内容。你的任务是准确地将自然语言描述转化为对应的Cypher查询语句,确保查询语法完全正确,并且能够执行成功。不要进行任何额外的分析或解释,只输出最终的Cypher查询语句。",
        "input": f"db_id: {item.get('db_id', 'unknown')}; {item.get('question', '')}",
        "history": [],
        "system": "你是一个自然语言至图查询语言翻译机器"
    })

# 保存为新的JSON文件
with open('./620ccf/data/AdvertiseGen/test.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)


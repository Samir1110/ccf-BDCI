############# 生成最终的格式
import json

# 读取jsonl文件并转换成json格式
jsonl_file = './620ccf/output/generated_predictions.jsonl'  # 原始jsonl文件路径
json_file = '/output/answer_cypher.json'   # 输出的json文件路径

# 创建一个空列表来存储转换后的数据
output_data = []

# 逐行读取jsonl文件并提取需要的字段
with open(jsonl_file, 'r', encoding='utf-8') as f:
    for index, line in enumerate(f):
        item = json.loads(line)
        # 提取predict字段并重新格式化为目标结构
        filtered_item = {
            "index": str(index),  # 将index转换为字符串
            "answer": item.get("predict", "")
        }
        output_data.append(filtered_item)

# 保存为新的json文件
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f'转换完成，输出文件：{json_file}')

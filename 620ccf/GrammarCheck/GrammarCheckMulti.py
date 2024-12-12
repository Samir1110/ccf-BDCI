import json
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from LcypherLexer import LcypherLexer
from LcypherParser import LcypherParser
import subprocess
import json

class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(SyntaxErrorListener, self).__init__()
        self.has_errors = False
        self.errors_message = ""

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.has_errors = True
        self.errors_message = f"Syntax error at line {line}, column {column}: {msg}"
        print(self.errors_message)


def check_syntax(input_text):
    input_stream = InputStream(input_text)
    lexer = LcypherLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = LcypherParser(token_stream)
    
    # 添加自定义错误监听器
    error_listener = SyntaxErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    
    # 使用语法的根规则 `oC_Cypher`
    parser.oC_Cypher()

    return error_listener.has_errors, error_listener.errors_message

def check_answers(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    errors = []
    for entry in data:
        index = entry.get("index")
        answer = entry.get("answer", "")
        
        if check_syntax(answer):
            errors.append(index)
            print(f"Syntax error found in answer with index {index}")
        else:
            print(f"No syntax error in answer with index {index}")
    
    if errors:
        print("\nAnswers with syntax errors:", errors)
    else:
        print("\nAll answers are syntactically correct.")

def check_answers_of_prediction(filename, error_file_path):
    with open(filename, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
    
    errors_index = [] 
    errors = []
    for i, entry in enumerate(data):
        answer = entry.get("predict")
        has_errors, errors_message = check_syntax(answer)
        if has_errors:
            input = f"原句：{answer} 错误原因：{errors_message}"
            output = entry.get("label") # fake
            error_entry = {
                "instruction": "你是一个TuGraph翻译修改机器,根据以下输入问题(input),修改成正确的答案,你应该生成对应的Cypher查询语句(output)。请确保你输出的结果必须只包含正确的Cypher查询语句,不要包含任何推测、注释或多余的内容。你的任务是准确地将有语法错误的输入修改成没有语法错误的输出,确保查询语法完全正确,并且能够执行成功。不要进行任何额外的分析或解释,只输出最终的Cypher查询语句。",
                "input": input,
                "output": output,
                "history": [],
                "system": "你是一个图查询语言修改机器"
            }
            errors.append(error_entry) 
            errors_index.append(i)           
            print(f"Syntax error found in answer with index {i}")
        else:
            print(f"No syntax error in answer with index {i}")
    
    if errors:
        print("\nAnswers with syntax errors amount:", len(errors))
        with open(error_file_path, 'w', encoding='utf-8') as f:
            json.dump(errors, f, ensure_ascii=False, indent=4)
        return errors_index
    else:
        print("\nAll answers are syntactically correct.")
        return None 


def replace_lines_with_new_data(original_file, new_data_file, indexes_to_replace, output_file):

    # 读取新数据文件
    with open(new_data_file, "r", encoding="utf-8") as new_file:
        new_data_lines = [json.loads(line) for line in new_file]
    
    # 读取原始文件并替换指定行
    updated_data = []
    with open(original_file, "r", encoding="utf-8") as orig_file:
        for i, line in enumerate(orig_file):
            if i in indexes_to_replace:
                # 查找索引对应的新数据
                index_in_new_data = indexes_to_replace.index(i)
                updated_data.append(new_data_lines[index_in_new_data])
            else:
                # 保留原始数据
                updated_data.append(json.loads(line))
    
    # 写入修改后的数据到新文件
    with open(output_file, "w", encoding="utf-8") as out_file:
        for record in updated_data:
            json.dump(record, out_file, ensure_ascii=False)
            out_file.write("\n")
    
    print(f"修改完成，保存至 {output_file}")




if __name__ == "__main__":
    complete_file = "./620ccf/output/generated_predictions.jsonl"
    error_file_path = "./620ccf/data/AdvertiseGen/error.json"
    error_correct_file = "./620ccf/output/error/generated_predictions.jsonl"
    patience = 5
    while patience > 0:
        error_index = check_answers_of_prediction(complete_file, error_file_path)
        if len(error_index) == 0:
            print(f"No error left, now patience is {patience}")
            break
        else:
            subprocess.run('bash ./620ccf/test_correct.sh', shell=True)
            replace_lines_with_new_data(complete_file, error_correct_file,error_index, complete_file)
            patience -= 1
            print(f"Error remains, attempting to try again, now patience is {patience}")

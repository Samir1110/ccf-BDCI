import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from GrammarCheck.LcypherLexer import LcypherLexer
from GrammarCheck.LcypherParser import LcypherParser

class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(SyntaxErrorListener, self).__init__()
        self.has_errors = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.has_errors = True
        print(f"Syntax error at line {line}, column {column}: {msg}")

def check_syntax(input_text):
    input_stream = InputStream(input_text)
    lexer = LcypherLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = LcypherParser(token_stream)
    
    # 添加自定义错误监听器
    error_listener = SyntaxErrorListener()
    parser.removeErrorListeners()  # 移除默认的错误监听器
    parser.addErrorListener(error_listener)
    
    # 使用语法的根规则 `oC_Cypher`
    parser.oC_Cypher()

    if error_listener.has_errors:
        print("There were syntax errors.")
    else:
        print("No syntax errors found.")

# 示例使用
if __name__ == "__main__":
    input_text = "MATCH (n:person) RETURN sum(n.born)"
    check_syntax(input_text)

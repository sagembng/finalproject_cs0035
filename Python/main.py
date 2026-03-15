from cp_lexer import tokenize
from cp_parser import Parser 
from cp_interpreter import Interpreter, SemanticError, RuntimeError_

def test_compiler(source_code, input_values=[]):
    print("--- Starting Compiler ---")
    
    # 1. Lexical Analysis
    tokens, lex_errors = tokenize(source_code)
    if lex_errors:
        print("Lex Errors:", lex_errors)
        return
        
    # 2. Syntax Analysis
    parser = Parser(tokens)
    statements, parse_errors = parser.parse()
    if parse_errors:
        print("Parse Errors:", parse_errors)
        return
        
    # 3. Semantic Analysis
    interpreter = Interpreter(input_values=input_values)
    semantic_errors = interpreter.check(statements)
    if semantic_errors:
        print("Semantic Errors:", semantic_errors)
        return
        
    # 4. Execution
    try:
        interpreter.execute(statements)
        print("Output Log:", interpreter.output_log)
        print("Symbol Table:", interpreter.symbol_table)
    except Exception as e:
        print("Runtime Error:", e)

if __name__ == '__main__':
    # Write some test code here!
    my_code = """
    var x;
    var y;
    x = 10;
    y = 20;
    output x;
    """
    
    test_compiler(my_code)
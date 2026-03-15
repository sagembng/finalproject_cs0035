from flask import Flask, render_template, request, jsonify
from cp_lexer import tokenize
from cp_parser import Parser
from cp_interpreter import Interpreter, SemanticError, RuntimeError_

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run', methods=['POST'])
def run_program():
    data = request.get_json()
    source_code = data.get('code', '')
    input_values_raw = data.get('inputs', [])

    result = {
        'tokens': [],
        'output': [],
        'errors': [],
        'symbol_table': {}
    }

    # --- Phase 1: Lexical Analysis ---
    tokens, lex_errors = tokenize(source_code)
    result['tokens'] = [f"({t[0]}, {t[1]})" for t in tokens]

    if lex_errors:
        result['errors'].extend(lex_errors)
        return jsonify(result)

    # --- Phase 2: Syntax Analysis ---
    parser = Parser(tokens)
    statements, parse_errors = parser.parse()

    if parse_errors:
        result['errors'].extend(parse_errors)
        return jsonify(result)

    # --- Phase 3: Semantic Analysis ---
    interpreter = Interpreter(input_values=input_values_raw)
    semantic_errors = interpreter.check(statements)

    if semantic_errors:
        result['errors'].extend(semantic_errors)
        return jsonify(result)

    # --- Phase 4: Execution ---
    try:
        interpreter.execute(statements)
        result['output'] = interpreter.output_log
        result['symbol_table'] = {
            k: (v if v is not None else 'uninitialized')
            for k, v in interpreter.symbol_table.items()
        }
    except (SemanticError, RuntimeError_) as e:
        result['errors'].append(f"Runtime Error: {e}")
    except Exception as e:
        result['errors'].append(f"Unexpected Error: {e}")

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
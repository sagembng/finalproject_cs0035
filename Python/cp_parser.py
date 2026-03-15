"""
Parser for the mini-compiler language.

Grammar (simplified):
  program     : statement*
  statement   : var_decl | input_stmt | output_stmt | assign_stmt
  var_decl    : 'var' IDENTIFIER ';'
  input_stmt  : 'input' IDENTIFIER ';'
  output_stmt : 'output' IDENTIFIER ';'
  assign_stmt : IDENTIFIER '=' expression ';'
  expression  : term (('+' | '-') term)*
  term        : factor (('*' | '/') factor)*
  factor      : NUMBER | IDENTIFIER | '(' expression ')'
"""


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type=None, expected_value=None):
        tok = self.peek()
        if tok is None:
            raise ParseError("Unexpected end of input")
        if expected_type and tok[0] != expected_type:
            raise ParseError(
                f"Expected token type '{expected_type}' but got '{tok[0]}' ('{tok[1]}')"
            )
        if expected_value and tok[1] != expected_value:
            raise ParseError(
                f"Expected '{expected_value}' but got '{tok[1]}'"
            )
        self.pos += 1
        return tok

    def parse(self):
        statements = []
        errors = []
        while self.peek() is not None:
            try:
                stmt = self.parse_statement()
                statements.append(stmt)
            except ParseError as e:
                errors.append(f"Syntax Error: {e}")
                # Skip to next semicolon for error recovery
                while self.peek() is not None and self.peek() != ('SYMBOL', ';'):
                    self.pos += 1
                if self.peek() == ('SYMBOL', ';'):
                    self.pos += 1
        return statements, errors

    def parse_statement(self):
        tok = self.peek()
        if tok is None:
            raise ParseError("Expected a statement but reached end of input")

        if tok == ('KEYWORD', 'var'):
            return self.parse_var_decl()
        elif tok == ('KEYWORD', 'input'):
            return self.parse_input_stmt()
        elif tok == ('KEYWORD', 'output'):
            return self.parse_output_stmt()
        elif tok[0] == 'IDENTIFIER':
            return self.parse_assign_stmt()
        else:
            raise ParseError(f"Unexpected token '{tok[1]}' — expected a statement")

    def parse_var_decl(self):
        self.consume('KEYWORD', 'var')
        name_tok = self.consume('IDENTIFIER')
        self.expect_semicolon()
        return ('VAR_DECL', name_tok[1])

    def parse_input_stmt(self):
        self.consume('KEYWORD', 'input')
        name_tok = self.consume('IDENTIFIER')
        self.expect_semicolon()
        return ('INPUT', name_tok[1])

    def parse_output_stmt(self):
        self.consume('KEYWORD', 'output')
        name_tok = self.consume('IDENTIFIER')
        self.expect_semicolon()
        return ('OUTPUT', name_tok[1])

    def parse_assign_stmt(self):
        name_tok = self.consume('IDENTIFIER')
        self.consume('SYMBOL', '=')
        expr = self.parse_expression()
        self.expect_semicolon()
        return ('ASSIGN', name_tok[1], expr)

    def expect_semicolon(self):
        tok = self.peek()
        if tok != ('SYMBOL', ';'):
            got = f"'{tok[1]}'" if tok else "end of input"
            raise ParseError(f"Expected ';' but got {got}")
        self.consume('SYMBOL', ';')

    # --- Expression parsing with precedence ---

    def parse_expression(self):
        """expression : term (('+' | '-') term)*"""
        left = self.parse_term()
        while self.peek() in [('SYMBOL', '+'), ('SYMBOL', '-')]:
            op = self.consume()[1]
            right = self.parse_term()
            left = ('BINOP', op, left, right)
        return left

    def parse_term(self):
        """term : factor (('*' | '/') factor)*"""
        left = self.parse_factor()
        while self.peek() in [('SYMBOL', '*'), ('SYMBOL', '/')]:
            op = self.consume()[1]
            right = self.parse_factor()
            left = ('BINOP', op, left, right)
        return left

    def parse_factor(self):
        """factor : NUMBER | IDENTIFIER | '(' expression ')'"""
        tok = self.peek()
        if tok is None:
            raise ParseError("Expected a value but reached end of input")

        if tok[0] == 'NUMBER':
            self.consume()
            return ('NUMBER', tok[1])
        elif tok[0] == 'IDENTIFIER':
            self.consume()
            return ('IDENTIFIER', tok[1])
        elif tok == ('SYMBOL', '('):
            self.consume('SYMBOL', '(')
            expr = self.parse_expression()
            self.consume('SYMBOL', ')')
            return expr
        else:
            raise ParseError(f"Unexpected token '{tok[1]}' in expression")
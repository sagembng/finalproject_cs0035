"""
Interpreter for the mini-compiler.
Performs semantic checks and executes the AST produced by the parser.
"""


class SemanticError(Exception):
    pass


class RuntimeError_(Exception):
    pass


class Interpreter:
    def __init__(self, input_values=None):
        """
        input_values: list of pre-supplied integers for 'input' statements.
                      Used in web mode so we don't block on stdin.
        """
        self.symbol_table = {}          # var_name -> value (int or None)
        self.output_log = []            # collected output lines
        self.input_values = list(input_values) if input_values else []
        self.input_index = 0
        self.errors = []

    # ------------------------------------------------------------------
    # Semantic Analysis
    # ------------------------------------------------------------------

    def check(self, statements):
        """Walk the AST and report semantic errors without executing."""
        declared = set()
        errors = []
        for stmt in statements:
            kind = stmt[0]
            if kind == 'VAR_DECL':
                _, name = stmt
                if name in declared:
                    errors.append(f"Semantic Error: Variable '{name}' already declared")
                declared.add(name)
            elif kind == 'INPUT':
                _, name = stmt
                if name not in declared:
                    errors.append(f"Semantic Error: Variable '{name}' used before declaration")
            elif kind == 'OUTPUT':
                _, name = stmt
                if name not in declared:
                    errors.append(f"Semantic Error: Variable '{name}' used before declaration")
            elif kind == 'ASSIGN':
                _, name, expr = stmt
                if name not in declared:
                    errors.append(f"Semantic Error: Variable '{name}' used before declaration")
                self._check_expr(expr, declared, errors)
        return errors

    def _check_expr(self, expr, declared, errors):
        kind = expr[0]
        if kind == 'NUMBER':
            pass
        elif kind == 'IDENTIFIER':
            name = expr[1]
            if name not in declared:
                errors.append(f"Semantic Error: Variable '{name}' used before declaration")
        elif kind == 'BINOP':
            _, op, left, right = expr
            self._check_expr(left, declared, errors)
            self._check_expr(right, declared, errors)

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(self, statements):
        for stmt in statements:
            self._exec_statement(stmt)

    def _exec_statement(self, stmt):
        kind = stmt[0]
        if kind == 'VAR_DECL':
            _, name = stmt
            self.symbol_table[name] = None
        elif kind == 'INPUT':
            _, name = stmt
            if name not in self.symbol_table:
                raise SemanticError(f"Variable '{name}' not declared")
            if self.input_index < len(self.input_values):
                val = self.input_values[self.input_index]
                self.input_index += 1
            else:
                raise RuntimeError_(f"Not enough input values provided for 'input {name}'")
            self.symbol_table[name] = int(val)
        elif kind == 'OUTPUT':
            _, name = stmt
            if name not in self.symbol_table:
                raise SemanticError(f"Variable '{name}' not declared")
            val = self.symbol_table[name]
            if val is None:
                raise RuntimeError_(f"Variable '{name}' has no value (never assigned)")
            self.output_log.append(str(val))
        elif kind == 'ASSIGN':
            _, name, expr = stmt
            if name not in self.symbol_table:
                raise SemanticError(f"Variable '{name}' not declared")
            val = self._eval_expr(expr)
            self.symbol_table[name] = val

    def _eval_expr(self, expr):
        kind = expr[0]
        if kind == 'NUMBER':
            return expr[1]
        elif kind == 'IDENTIFIER':
            name = expr[1]
            if name not in self.symbol_table:
                raise SemanticError(f"Variable '{name}' not declared")
            val = self.symbol_table[name]
            if val is None:
                raise RuntimeError_(f"Variable '{name}' has no value (never assigned)")
            return val
        elif kind == 'BINOP':
            _, op, left, right = expr
            lval = self._eval_expr(left)
            rval = self._eval_expr(right)
            if op == '+':
                return lval + rval
            elif op == '-':
                return lval - rval
            elif op == '*':
                return lval * rval
            elif op == '/':
                if rval == 0:
                    raise RuntimeError_("Division by zero")
                return lval // rval
        raise RuntimeError_(f"Unknown expression type: {kind}")
import re

KEYWORDS = {'var', 'input', 'output'}

TOKEN_PATTERNS = [
    ('COMMENT',    r'/\*.*?\*/'),
    ('NUMBER',     r'\d+'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('SYMBOL',     r'[+\-*/=();]'),
    ('SKIP',       r'[ \t\n\r]+'),
    ('MISMATCH',   r'.'),
]

MASTER_PATTERN = re.compile(
    '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_PATTERNS),
    re.DOTALL
)


def tokenize(source_code):
    tokens = []
    errors = []
    line_num = 1

    for mo in MASTER_PATTERN.finditer(source_code):
        kind = mo.lastgroup
        value = mo.group()
        line_num += value.count('\n')

        if kind == 'COMMENT':
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'NUMBER':
            tokens.append(('NUMBER', int(value)))
        elif kind == 'IDENTIFIER':
            if value in KEYWORDS:
                tokens.append(('KEYWORD', value))
            else:
                tokens.append(('IDENTIFIER', value))
        elif kind == 'SYMBOL':
            tokens.append(('SYMBOL', value))
        elif kind == 'MISMATCH':
            errors.append(f"Lexical Error (line ~{line_num}): Unexpected character '{value}'")

    return tokens, errors
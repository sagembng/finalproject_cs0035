# finalproject_cs0035
A web-based mini-compiler featuring a custom lexer, parser, and interpreter. Built with Python, Flask, and a custom white creamy themed UI for CS0035.

# 🍔 Allison Burgers — Mini Compiler

> A mini compiler/interpreter for a custom programming language, built with Python and Flask.  
> **CS0035 – Programming Languages | Section TN31**

---

## 👥 Group Members

| Name | Role |
|---|---|
| Kiarash Shamspour | Developer |
| Xavier Imbang | Developer |

---

## 📌 Project Overview

This project implements a full compiler pipeline for a small, custom programming language. It reads source code written in the language, processes it through each stage of the compiler pipeline, and executes the program — all through a web-based interface running on localhost.

**Compiler Pipeline:**
```
Source Code → Lexical Analysis → Syntax Parsing → Semantic Check → Execution → Output
```

---

## 🗂️ Project Structure

```
mini_compiler/
├── app.py                  ← Flask web server (entry point)
├── lexer.py                ← Lexical analyzer (tokenizer)
├── syntax_parser.py        ← Syntax parser + AST builder
├── interpreter.py          ← Semantic checker + AST executor
├── requirements.txt        ← Python dependencies
├── sample_program.txt      ← Example source program
├── README.md               ← You are here
└── templates/
    └── index.html          ← Web UI (served by Flask)
```

---

## ⚙️ Requirements

- Python 3.8 or higher
- Flask 2.3.0 or higher

Install dependencies:
```bash
pip install -r requirements.txt
```

Or using `py` on Windows:
```bash
py -m pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
cd mini_compiler
python app.py
```

On Windows:
```bash
py app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

> **Note:** No XAMPP or any external server is needed. Flask runs its own built-in development server.

---

## 🌐 Web Interface Features

- **Source Code Editor** — Write or paste your program directly in the browser, with live line numbers
- **Input Values** — Supply space-separated integers for `input` statements before running
- **Run Program** — Executes the full compiler pipeline on click (or press `Ctrl+Enter`)
- **Token Stream** — Displays all tokens produced by the lexer, color-coded by type
- **Program Output** — Shows the result of all `output` statements
- **Errors Panel** — Reports lexical, syntax, semantic, and runtime errors with clear messages
- **Symbol Table** — Shows all declared variables and their current values after execution
- **Pipeline Indicator** — Highlights which stage of the compiler is active or where an error occurred
- **Example Programs** — Load pre-built examples with one click (Basic I/O, Arithmetic, Parentheses, Syntax Error, Undeclared Variable)

---

## 📖 Language Specification

### Supported Keywords

| Keyword | Description |
|---|---|
| `var` | Declares a variable |
| `input` | Reads an integer value from the user |
| `output` | Prints the value of a variable |

### Rules

- All statements must end with a **semicolon** `;`
- All variables must be **declared before use** with `var`
- All values are **integers only**
- Whitespace is not significant
- Comments use `/* block comment */` syntax and may span multiple lines

### Operators

| Operator | Description |
|---|---|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Integer division |
| `=` | Assignment |
| `( )` | Grouping / precedence |

Operator precedence follows standard math rules: `*` and `/` are evaluated before `+` and `-`.

### Variable Naming

- Letters, numbers, and underscores are allowed
- Cannot start with a number
- Valid: `x`, `value1`, `_total`
- Invalid: `1x`

---

## 💻 Example Program

```
/* Compute a weighted sum */
var x;
var y;
var z;

input x;
input y;

z = x + y * 2;

output z;
```

Given inputs `3` and `4`, this outputs `11` (because `3 + 4 * 2 = 11` by operator precedence).

---

## 🛠️ Compiler Stages

### 1. Lexer (`lexer.py`)
Converts raw source code into a flat list of tokens. Strips comments and classifies each token as:
- `KEYWORD` — `var`, `input`, `output`
- `IDENTIFIER` — variable names
- `NUMBER` — integer literals
- `SYMBOL` — operators and punctuation

### 2. Parser (`syntax_parser.py`)
Validates the token stream against the language grammar using a recursive-descent parser. Produces an Abstract Syntax Tree (AST). Handles operator precedence and parentheses correctly. Reports syntax errors such as missing semicolons or malformed expressions.

### 3. Semantic Analyzer (`interpreter.py`)
Walks the AST before execution to check for semantic errors — primarily ensuring all variables are declared before they are used in assignments or output statements.

### 4. Interpreter (`interpreter.py`)
Executes the AST by walking each node, evaluating expressions recursively, maintaining a symbol table of variable values, and handling `input` and `output` statements.

---

## 🧪 Error Detection

The compiler detects and reports errors at each stage:

| Error Type | Example |
|---|---|
| Lexical Error | Unexpected character like `@` |
| Syntax Error | Missing semicolon: `x = 5` |
| Semantic Error | Undeclared variable: `output y;` without `var y;` |
| Runtime Error | Division by zero, uninitialized variable |

---

## 📋 Sample Test Cases

| Program | Input | Expected Output |
|---|---|---|
| `var x; input x; output x;` | `42` | `42` |
| `var x; var y; var z; x = 3; y = 4; z = x + y * 2; output z;` | *(none)* | `11` |
| `var x; var y; var z; input x; input y; z = (x + y) * 2; output z;` | `5 3` | `16` |
| `var x; x = 10 output x;` | *(none)* | Syntax Error: missing `;` |
| `output y;` | *(none)* | Semantic Error: undeclared variable |

---

## 📚 Course Information

- **Course:** CS0035 – Programming Languages
- **Section:** TN31
- **Group Name:** Allison Burgers
- **Project Type:** Mini Compiler / Interpreter

# Code Review Report

Quality Score: 0/100

## CRITICAL — hardcoded-secret

Line: 9

Possible hardcoded secret detected.

Suggestion: Move secrets to environment variables or a dedicated secrets manager.

## CRITICAL — hardcoded-secret

Line: 10

Possible hardcoded secret detected.

Suggestion: Move secrets to environment variables or a dedicated secrets manager.

## CRITICAL — hardcoded-secret

Line: 11

Possible hardcoded secret detected.

Suggestion: Move secrets to environment variables or a dedicated secrets manager.

## HIGH — dangerous-eval

Line: 35

eval() can execute arbitrary Python code.

Suggestion: Avoid eval(). If you only need Python literals, consider ast.literal_eval().

## HIGH — dangerous-eval

Line: 198

eval() can execute arbitrary Python code.

Suggestion: Avoid eval(). If you only need Python literals, consider ast.literal_eval().

## HIGH — dangerous-exec

Line: 37

exec() can execute arbitrary code.

Suggestion: Replace dynamic execution with explicit functions or safe parsing.

## HIGH — subprocess-shell

Line: 45

subprocess call uses shell=True.

Suggestion: Prefer shell=False and pass arguments as a list, especially when handling user input.

## MEDIUM — bare-except

Line: 199

Bare except catches every exception.

Suggestion: Catch specific exception types such as ValueError or OSError.

## MEDIUM — bare-except

Line: 268

Bare except catches every exception.

Suggestion: Catch specific exception types such as ValueError or OSError.

## MEDIUM — bare-except

Line: 24

Bare except catches every exception.

Suggestion: Catch specific exception types such as ValueError or OSError.

## MEDIUM — mutable-default

Line: 14

Mutable default arguments can preserve state between calls.

Suggestion: Use None as the default and create the object inside the function.

## MEDIUM — mutable-default

Line: 105

Mutable default arguments can preserve state between calls.

Suggestion: Use None as the default and create the object inside the function.

## MEDIUM — long-function

Line: 105

Function 'process_customer' is 59 lines long.

Suggestion: Split the function into smaller single-responsibility functions.

## MEDIUM — long-function

Line: 216

Function 'massive_function' is 47 lines long.

Suggestion: Split the function into smaller single-responsibility functions.

## MEDIUM — high-complexity

Line: 105

Function 'process_customer' has estimated complexity 18.

Suggestion: Reduce branching or extract logic into smaller functions.

## LOW — debug-print

Line: 27

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 33

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 43

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 68

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 106

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 167

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 185

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 217

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 260

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 273

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 294

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 112

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 115

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 118

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 131

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 134

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 137

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 149

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 152

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 155

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 182

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 223

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 226

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 244

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 247

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 250

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 284

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 269

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 128

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 124

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — debug-print

Line: 126

print() may be leftover debugging or unsuitable for production logging.

Suggestion: Use Python's logging module for structured application logs.

## LOW — unused-import

Line: 4

Import 'math' does not appear to be used.

Suggestion: Remove unused imports to keep dependencies and code clean.

## LOW — unused-import

Line: 7

Import 'random' does not appear to be used.

Suggestion: Remove unused imports to keep dependencies and code clean.

## LOW — open-without-context

Line: 92

File opened without a context manager.

Suggestion: Use 'with open(...) as file:' to ensure the file is closed.

## LOW — open-without-context

Line: 100

File opened without a context manager.

Suggestion: Use 'with open(...) as file:' to ensure the file is closed.

## LOW — open-without-context

Line: 173

File opened without a context manager.

Suggestion: Use 'with open(...) as file:' to ensure the file is closed.

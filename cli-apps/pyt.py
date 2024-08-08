from os import system
import sys
import subprocess
import time
import re
ALLOWED_FILES = [".py"]
INTER_FILENAME = "status.txt"

### COMPLEXITY FUNCTION ###
import ast

class ComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.complexity = {}
        self.current_scope = "global"  # Handle global scope
        self.complexity[self.current_scope] = "O(1)"  # Start with O(1) for global scope

    def visit_FunctionDef(self, node):
        self.current_scope = node.name
        self.complexity[self.current_scope] = "O(1)"  # Start with O(1) for the function
        self.generic_visit(node)
        self.current_scope = "global"  # Reset to global scope after visiting function

    def visit_For(self, node):
        if self.current_scope:
            self.complexity[self.current_scope] = self._increase_complexity(self.complexity[self.current_scope])
        self.generic_visit(node)

    def visit_While(self, node):
        if self.current_scope:
            self.complexity[self.current_scope] = self._increase_complexity(self.complexity[self.current_scope])
        self.generic_visit(node)

    def visit_Call(self, node):
        if self.current_scope:
            func_name = self._get_function_name(node)
            if func_name == self.current_scope:  # Recursive call
                self.complexity[self.current_scope] = self._increase_complexity(self.complexity[self.current_scope], recursive=True)
        self.generic_visit(node)

    def _increase_complexity(self, complexity, recursive=False):
        if complexity == "O(1)":
            return "\033[92mO(n)\033[0m"
        elif complexity == "O(n)":
            return "\033[93mO(n^2)\033[0m" if not recursive else "\033[93mO(n^n)\033[0m"
        elif complexity == "O(n^2)":
            return "\033[91mO(n^3)\033[0m"
        else:
            return "\033[90mO(?)\033[0m"  # Too complex to analyze simply

    def _get_function_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None

    def report(self,filename):
        max_len = max(len(scope) for scope in self.complexity.keys())
        #print(f"\n  \033[1m{filename.upper()}\033[0m Functions Time Complexities\n")
        print(f"\nComplexity Analysis\n")
        func_counter = 0
        for scope, complexity in self.complexity.items():
            func_counter+=1
            func_counter = str(func_counter)
            if len(func_counter) < 2:
                func_spacer = " "
            elif len(func_counter) == 2:
                func_spacer = ""
            func_counter = int(func_counter)
            scope_name = "global scope" if scope == "global" else f"{scope}"
            print(f"  {func_spacer}\033[90m{func_counter} | \033[30m{scope_name:<{max_len + 10}} \033[92m{complexity}")

def analyze_complexity(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read())
    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)
    analyzer.report(filename)



class ScriptAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {
            "lines_of_code": 0,
            "functions": 0,
            "classes": 0,
            "loops": 0,
            "conditionals": 0,
            "function_calls": 0,
            "recursions": 0
        }
        self.current_scope = "global"

    def visit_FunctionDef(self, node):
        self.stats["functions"] += 1
        self.current_scope = node.name
        self.generic_visit(node)
        self.current_scope = "global"

    def visit_ClassDef(self, node):
        self.stats["classes"] += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.stats["loops"] += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.stats["loops"] += 1
        self.generic_visit(node)

    def visit_If(self, node):
        self.stats["conditionals"] += 1
        self.generic_visit(node)

    def visit_Call(self, node):
        self.stats["function_calls"] += 1
        func_name = self._get_function_name(node)
        if func_name and func_name == self.current_scope:
            self.stats["recursions"] += 1
        self.generic_visit(node)

    def visit(self, node):
        self.stats["lines_of_code"] += 1
        super().visit(node)

    def _get_function_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None

    def report(self, filename):
        max_len = max(len(scope) for scope in self.stats.keys())
        print(f"\n\033[0mScript Analysis\n")
        
        func_counter = 0
        for key, value in self.stats.items():
            func_counter += 1
            func_counter_str = str(func_counter)
            func_spacer = " " * (2 - len(func_counter_str)) if len(func_counter_str) < 2 else ""
            
            # Mapping stats key to readable format
            readable_key = key.replace('_', ' ').title()
            
            # Print the result in the specified format
            print(f"  {func_spacer}\033[90m{func_counter_str} | \033[30m{readable_key:<{max_len + 10}} \033[92m{value}")

def analyze_script(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read())
    analyzer = ScriptAnalyzer()
    analyzer.visit(tree)
    analyzer.report(filename)
### END OF FUNCTION ###


def get_file_args():
    """
    This Translates The Args And Makes Them Usable
    """
    args = []
    for i in range(1, min(10, len(sys.argv))):  # Start from 1 to skip the script name
        if sys.argv[i]:
            args.append(sys.argv[i])
        else:
            print("False")
    return args

def get_errors(filename):
    result = subprocess.run(
        ["python", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    if result.stderr:
        with open(INTER_FILENAME, "w") as error_file:
            error_file.write(result.stderr)
        return True
    else:
        return False
    
def inspect_file(filename):
    errors = []
    with open(INTER_FILENAME, "r") as file:
        lines = file.readlines()
        
        i = 0
        while i < len(lines):
            if lines[i].startswith('  File '):
                error_info = lines[i].strip()
                variable_line = ""
                error_desc_lines = []

                # Extract line number using regex
                match = re.search(r'line (\d+)', error_info)
                if match:
                    line_number = match.group(1)
                else:
                    line_number = "Unknown"

                # Variable line (if present)
                if i + 1 < len(lines) and not lines[i + 1].startswith('  File '):
                    variable_line = lines[i + 1].strip()
                    i += 1

                # Collecting error description lines
                while i < len(lines) and not lines[i].startswith('  File ') and lines[i].strip():
                    error_desc_lines.append(lines[i].strip())
                    i += 1

                error_desc = " ".join(error_desc_lines).strip()

                errors.append((line_number, variable_line, error_desc))
            else:
                i += 1

    return errors

def show_term_display(errors,filename):
    """
    This Shows The "IDE" Styled Of Error Displays.
    Input,
        errors -> the errors scanned from the files
        filename -> the file to read / debug
    Return,
        time -> Elapsed Time
    """
    time_start = time.time()
    for error in errors:
     error_message_index = error[2].rfind("^")
     error_message = error[2][error_message_index+2:]
    print(f"\033[47m\033[91m ERR! \033[0m\033[91m 1 or More Errors Detected\033[0m\n\033[33m {{ \033[0m {error_message} \033[33m }} \033[0m \n")
    # Read the entire file content into a list of lines
    with open(filename, 'r', encoding='utf-8') as file:
        lines = [line.rstrip() for line in file]

    # Determine the maximum number of digits in the line numbers
    max_line_number_length = len(str(len(lines)))

    def format_line_number(line_number):
        """Format the line number with padding to align columns."""
        return f"{line_number:>{max_line_number_length}}"

    for error in errors:
        error_line_num = int(error[0]) - 1  # Adjust for 0-based indexing

        # Determine the context lines
        pre_line = max(0, error_line_num - 1)
        curr_line = error_line_num
        post_line = min(len(lines) - 1, error_line_num + 1)

        # Display previous line if it exists
        if pre_line < curr_line:
            print(f'    \033[90m{format_line_number(pre_line + 1)}\033[0m | {lines[pre_line]}')

        # Display current line with error indicator
        print(f'\033[91m->  \033[90m{format_line_number(curr_line + 1)}\033[0m | {lines[curr_line]}')

        # Display next line if it exists
        if post_line > curr_line:
            print(f'    \033[90m{format_line_number(post_line + 1)}\033[0m | {lines[post_line]}')
    time_end = time.time()
    return time_end - time_start


def make_shortcut():
    with open("pyt.cmd", "w") as file:
        file.write("@echo off\nchcp 65001>nul && setlocal enabledelayedexpansion\npython pyt.py %1")
    return True

def filearg_analysis(filearg):
    if filearg == "-sc":
        stat = make_shortcut()
        if stat == True:
            print(f"\033[92m OK! \033[0m\033[0mSuccessfully Created A Shortcut!\n\n\033[90mTIP!\n   For Windows Users, Set This Sortcut (Ending With .cmd Inside\n   Your Windows Dir 'C:\\Windows' Along With 'pyt.py' For Easy Acces!\033[0m")
    elif filearg == "-tc":
        return "complexity_true"
    elif filearg == "-ss":
        return "summary_true"
    elif filearg == "-st":
        return "startup_true"
    elif filearg == "-ns":
        return "normal_scan"
    else:
        return "none"
    
def prog_help():
    print("\nWelcome To PYT (Python Trace)\nThe Better Python Error Tool; Transforming hard to read error messages \ninto better visualized feedback!")
    print("\nUsage:  pyt < -ARG > < FILENAME >")
    print("\nArgs Help,\n-sc    Create A Shortcut\n-tc    Show Time Complexity\n-ss    Show Script Summary\n-st    Start Script\n-ns    Normal Scan")

def main():
    try:
        file_arg = sys.argv[1]
        if file_arg == "-?":
            prog_help()
            sys.exit(1)
        rule = filearg_analysis(file_arg)
        if rule == "none":
            #print("\033[91mERR! \033[0mPlease enter a valid arguement. \033[90m'-ns for normal start'\033[0m")
            #sys.exit(1)
            print("\033[90mNo Start Rule Set; Starting in Normal Mode\n")
            filename = sys.argv[1]
        else:
            filename = sys.argv[2]
    except IndexError:
        print("\033[91mERR! \033[0mPlease enter a file.")
        sys.exit(1)
    fileexit = filename[filename.rfind("."):]
    if fileexit not in ALLOWED_FILES:
        print("\033[91mERR! \033[0mPlease enter a valid Python File.")
        sys.exit(1)
    else:
        bool_verify = get_errors(filename)
        #print(bool_verify)
        if bool_verify == True:
            errors = inspect_file(filename)
            runtime = show_term_display(errors,filename)    
        else:
            print(f"\033[47m\033[92m OK! \033[0m\033[92m {filename.upper()} Has No Errors!\033[0m")
            if rule == "complexity_true":
                analyze_complexity(filename)
            elif rule == "summary_true":
                analyze_script(filename)
            elif rule == "startup_true":
                print(f"\033[90m\nStarting {filename} In A New Window")
                system(f"start python {filename}")
    ### Clean UP ###
    #os.remove(INTER_FILENAME)
    
if __name__ == "__main__":
    main()

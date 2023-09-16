#!/usr/bin/python3

import ast
import argparse
import re
import sys
import os
import importlib.util
from importlib.util import spec_from_loader
from importlib.abc import MetaPathFinder
from importlib.machinery import SourceFileLoader
from tempfile import NamedTemporaryFile
from collections import Counter
import traceback

#=========================================================================
# Used to hook and redirect imports to the TMP modules with yokai syntax replacement

class ImportRedirector(MetaPathFinder):
    def __init__(self, redirect_module_name, redirect_module_path):
        self.redirect_module_name = redirect_module_name
        self.redirect_module_path = redirect_module_path

    def find_spec(self, fullname, path, target=None):
        if fullname == self.redirect_module_name:
            loader = SourceFileLoader(fullname, self.redirect_module_path)
            return spec_from_loader(loader.name, loader)

        return None

#=========================================================================
# Yokai Syntax Replacement Functions

def syntax_replacement(code):
    #n_pattern = re.compile(r'\\n')
    code = code.replace('\\', '\\\\')

    # Apply the BASH and PYTHON pattern replacements
    bash_pattern = re.compile(r'(\s*)bash:\s*(f?["\'].*?["\'])')
    code = bash_pattern.sub(r'\1yokai_return.commands.append(self.__run_bash_command__(yokai.BASH(\2)))', code)

    python_assignment_pattern = re.compile(r'^(\s*)python:\s*([a-zA-Z_][a-zA-Z0-9_]*)*\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\)', re.DOTALL | re.MULTILINE)
    code = python_assignment_pattern.sub(r'\1yokai_return.commands.append(self.__run_python_function__(yokai.PYTHON(\3, \4)))\n\1\2 = r.commands[-1].returned', code)

    python_pattern = re.compile(r'python:\s*([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\)')
    code = python_pattern.sub(r'yokai_return.commands.append(self.__run_python_function__(yokai.PYTHON(\1, \2)))', code)

    # Apply the yokai function pattern replacement
    code = yokai_replacement(code)

    code = code.replace('\\\\', '\\')
    return code


def yokai_replacement(code):
    yokai_pattern = re.compile(r'^([ \t]*?)yokai\s+([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\):', re.DOTALL | re.MULTILINE)
    for def_match in yokai_pattern.findall(code):

        init_indent = def_match[0]
        func_name = def_match[1]
        func_args = def_match[2]

        # Get the entire yokai function definition
        #                                   rf"^{indent}yokai yki_func2\(\):.*$(?:\n(?!{indent}\S).*|\s*$)*(?=\n{indent}\S|\Z)"
        #                                   rf"^{init_indent}yokai\s+{func_name}\({func_args}\):.*$(?:\n\s*)*(?:\n(?!{init_indent}\S).*|\s*$)*(?=\n{init_indent}\S|\Z)"
        yokai_function_pattern = re.compile(rf"^{init_indent}yokai\s+{func_name}\({func_args}\):.*$(?:\n\s*)*(?:\n(?!{init_indent}\S).*|\s*$)*(?=\n{init_indent}\S|\Z)", re.MULTILINE)
        func = yokai_function_pattern.findall(code)[0]

        # Get just the body
        func_body = re.findall(rf"^{init_indent}yokai\s+{func_name}\({func_args}\):\n(.+)", func, re.DOTALL | re.MULTILINE)[0]

        # Get the first non-blank lines indent 
        line_indent = re.findall('^([ \t]+)\S.+$', func_body, re.MULTILINE)[0]
        indent = line_indent[0] * (len(line_indent) - len(init_indent))

        new_func = ""
        new_func += f"{init_indent}class {func_name}(yokai.Yokai):\n"
        new_func += f"{init_indent}{indent}def __execute__(self, {func_args}):\n{init_indent}{indent*2}yokai_return = yokai.YKI(self.__class__.__name__, self.scheduler)\n"
        for line in func_body.split('\n'):
            if not line == '':
                new_func += f"{indent}{line}\n"

        return_pattern = re.compile(r"([ \t]*)return.+")
        code = return_pattern.sub(r'\1return r', code)

        new_func += f"{init_indent}{indent*2}return yokai_return\n"

        code = yokai_function_pattern.sub(new_func, code)

    return code



#=========================================================================

def get_module_name(file_path):
    module_name, _ = os.path.splitext(os.path.basename(file_path))
    return module_name

def collect_module_paths(file_path, seen_modules=None, yokai_modules=None):
    if seen_modules is None:
        seen_modules = set()
    
    if yokai_modules is None:
        yokai_modules = {}

    try:
        with open(file_path, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        return None, None
    except UnicodeDecodeError:
        return None, None
    
    yokai_function_pattern = re.compile(r'\byokai\b\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)\s*:(.*?)(?=^\s*yokai\b|^\s*$|\Z)', re.DOTALL | re.MULTILINE)
    if bool(yokai_function_pattern.search(code)):
        code = syntax_replacement(code)

        yokai_modules[get_module_name(file_path)] = file_path

    tree = ast.parse(code, file_path)
    local_imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                local_imports.add(n.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module
            if module:
                local_imports.add(module)

    seen_modules.update(local_imports)

    for module in local_imports:
        try:
            spec = importlib.util.find_spec(module)
            if spec and spec.origin and spec.origin != file_path and os.path.isfile(spec.origin) and spec.origin not in seen_modules:
                seen_modules.add(spec.origin)
                collect_module_paths(spec.origin, seen_modules, yokai_modules)
        except:
            continue

    return yokai_modules
    
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[name] = module
    return module

def transform_module_code(module_paths):
    temp_module_paths = {}
    for module_name, module_path in module_paths.items():
        try:
            with open(module_path, 'r') as file:
                code = file.read()
        except FileNotFoundError:
            print(f"No such file: '{os.path.abspath(module_path)}'")
            continue
        
        # Applying syntax replacement before saving the transformed code back to a temporary file
        transformed_code = syntax_replacement(code)
        
        with NamedTemporaryFile(mode='w+', delete=False, suffix='.py') as temp:
            temp.write(transformed_code)
            temp_module_paths[module_name] = temp.name

    return temp_module_paths

def cleanup_temp_files(temp_modules):
    for _, temp_module_path in temp_modules.items():
        try:
            os.unlink(temp_module_path)
        except Exception as e:
            print(f"Failed to delete temporary file {temp_module_path}: {e}")

#-------------------------------------------------------------------------

def execute_file(file_path):
    try:
        module_paths = collect_module_paths(file_path)
        temp_module_paths = transform_module_code(module_paths)

        for temp_module_name, temp_module_path in temp_module_paths.items():
            sys.meta_path.insert(0, ImportRedirector(temp_module_name, temp_module_path))

        new_main_script_path = temp_module_paths[file_path.replace('.py','')]
        load_module('__main__', new_main_script_path)

    except FileNotFoundError:
        print(f"No such file: '{os.path.abspath(file_path)}'")
        traceback.print_exc()
    except Exception as e:
        print(f"An error occurred while executing the file: {e}")
        traceback.print_exc()
    finally:
        # Cleanup temporary files
        #cleanup_temp_files(temp_module_paths)
        pass

#=========================================================================

def main():
    parser = argparse.ArgumentParser(description="Execute a Python file with AST transformations.")
    parser.add_argument("file_path", help="Path to the Python file to execute")
    args = parser.parse_args()
    try:
        execute_file(args.file_path)
    except SyntaxError as e:
        #print(e)
        pass


if __name__ == "__main__":
    main()
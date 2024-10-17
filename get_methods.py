import os
import ast
from collections import defaultdict
import fnmatch

ignored = [
    "__pycache__/",
    "*.py[cod]",
    "*$py.class",
    "*.so",
    ".Python",
    "build/",
    "develop-eggs/",
    "dist/",
    "downloads/",
    "eggs/",
    ".eggs/",
    "lib/",
    "lib64/",
    "parts/",
    "sdist/",
    "var/",
    "wheels/",
    "pip-wheel-metadata/",
    "share/python-wheels/",
    "*.egg-info/",
    ".installed.cfg",
    "*.egg",
    "MANIFEST",
    "*.manifest",
    "*.spec",
    "pip-log.txt",
    "pip-delete-this-directory.txt",
    "htmlcov/",
    ".tox/",
    ".nox/",
    ".coverage",
    ".coverage.*",
    ".cache",
    "nosetests.xml",
    "coverage.xml",
    "*.cover",
    ".hypothesis/",
    ".pytest_cache/",
    "*.mo",
    "*.pot",
    "*.log",
    "local_settings.py",
    "db.sqlite3",
    "instance/",
    ".webassets-cache",
    ".scrapy",
    "truguard_api/openapi/_build/",
    "target/",
    ".ipynb_checkpoints",
    "profile_default/",
    "ipython_config.py",
    ".python-version",
    "celerybeat-schedule",
    "*.sage.py",
    ".env",
    ".envrc",
    ".venv",
    "env/",
    "venv/",
    "ENV/",
    "env.bak/",
    "venv.bak/",
    ".spyderproject",
    ".spyproject",
    ".ropeproject",
    "/site",
    ".mypy_cache/",
    ".dmypy.json",
    "dmypy.json",
    ".pyre/",
    ".idea",
    "tags",
    ".swp",
    ".vscode",
    ".DS_Store",
]

def get_definitions(directory, use_absolute_path=True):
    definitions_map = defaultdict(list)
    for root, dirs, files in os.walk(directory):
        # Exclude directories that should be ignored
        dirs[:] = [
            d for d in dirs
            if not any(
                fnmatch.fnmatch(os.path.relpath(os.path.join(root, d), directory), pattern)
                for pattern in ignored
            )
        ]
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(file_path, directory)
                if any(fnmatch.fnmatch(rel_file_path, pattern) for pattern in ignored):
                    continue
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read(), filename=file_path)
                        # Collect definitions
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                                definition_type = 'class' if isinstance(node, ast.ClassDef) else 'function'
                                name = node.name
                                start_line = node.lineno
                                end_line = getattr(node, 'end_lineno', start_line)
                                key = os.path.abspath(file_path) if use_absolute_path else rel_file_path
                                definitions_map[key].append({
                                    'type': definition_type,
                                    'name': name,
                                    'start_line': start_line,
                                    'end_line': end_line
                                })
                    # Ensure the file is included even if no definitions were found
                    key = os.path.abspath(file_path) if use_absolute_path else rel_file_path
                    definitions_map.setdefault(key, [])
                except (UnicodeDecodeError, SyntaxError) as e:
                    print(f"Error processing file {file_path}: {e}")
                    continue
    return dict(definitions_map)




# Example usage:
# project_dir = './truguard_api/'
# methods_map = get_methods(project_dir)
# print(methods_map)


def get_method(file_path, method_info):
    """
    Extract the lines of a specific method from a file.
    
    :param file_path: The path to the Python file
    :param method_info: A dictionary containing 'name', 'start_line', and 'end_line' of the method
    :return: A string containing the method's code
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            # Extract the relevant lines
            method_lines = lines[method_info['start_line']-1:method_info['end_line']]
            
            # Join the lines and strip any leading/trailing whitespace
            method_code = ''.join(method_lines).strip()
            
            return method_code
    except FileNotFoundError:
        return f"Error: File not found - {file_path}"
    except IOError:
        return f"Error: Unable to read file - {file_path}"


def get_methods_with_code(methods_map):
    methods_with_code = {}
    for file_path, methods in methods_map.items():
        methods_with_code[file_path] = []
        for method in methods:
            method_code = get_method(file_path, method)
            method_info = method.copy()  # Create a copy of the original method info
            method_info['method_code'] = method_code
            methods_with_code[file_path].append(method_info)
    return methods_with_code


if __name__ == "__main__":
    project_dir = './test/'
    methods_map = get_methods(project_dir)
    methods_with_code = get_methods_with_code(methods_map)
    print(methods_with_code)

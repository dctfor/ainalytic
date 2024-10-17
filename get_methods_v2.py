import os
import ast
from collections import defaultdict

ignored= [
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

def get_methods( directory, use_absolute_path=True):
    methods_map  = defaultdict(list)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file not in ignored:
                file_path  = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        tree  = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                method_name  = node.name
                                if use_absolute_path:
                                    methods_map[os.path.abspath(file_path)].append(method_name)
                                else:
                                    methods_map[os.path.relpath(file_path)].append(method_name)
                except UnicodeDecodeError as e:
                    print(f"Error decoding file {file_path}: {e}")
                    continue
    return dict(methods_map)


# Example usage:
# project_dir = './truguard_api/'
# methods_map = get_methods(project_dir)
# print(methods_map)
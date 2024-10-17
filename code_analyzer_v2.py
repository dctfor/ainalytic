import logging
import os
import sys
from constants import doc_prompt
from get_methods import get_definitions
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

init_history = [
    {"role": "system", "content": "You are a Python code documentation expert. Analyze the provided code and generate comprehensive documentation without enhancing or changing the code. Be concise but informative."},
#     {"role": "user", "content": """Analyze Python class methods and provide the following for each:
# 1. `method_name(parameters)`:
#    - Parameters: param1 (type): description, param2 (type): description
#    - Related Methods Within: method1, method2, method3
#    - Return Type: return_type
#    - Docstring: Brief description of method's purpose.
#    - Key libraries or dependencies used.
# Use "None" for no parameters or returns. Be concise but informative."""},
]

history = init_history

msg = ''
def get_last_folder_name(path):
    return os.path.basename(os.path.normpath(path))

if len(sys.argv) != 2:
    logging.error("Usage: python code_analyzer_v2.py <project_path>")
    sys.exit(1)

project_path = sys.argv[1]

file_output = f"{get_last_folder_name(project_path)}.txt"

files_and_methods = get_definitions(project_path, use_absolute_path=True)
logging.info(f"Found {len(files_and_methods.keys())} files")
errors = []
# Check if the file exists
if not os.path.exists(file_output):
    # If the file doesn't exist, create it by opening it in write mode
    with open(file_output, 'w') as file:
        pass

with open(file_output, 'r') as file:
    lines = file.readlines()

# Initialize an empty set to store the file paths
file_paths = set()

# Process each line
for line in lines:
    # If the line starts with 'FILE:', extract the file path
    if line.startswith('FILE:'):
        file_path = line[5:].strip()  # Remove 'FILE:' and any leading/trailing whitespace
        file_paths.add(file_path)

files_and_methods = {path: methods for path, methods in files_and_methods.items() if path not in file_paths}
logging.info(f"Will process {len(files_and_methods.keys())} files")

for path in files_and_methods.keys():
    logging.info(f"Processing File: {path} ...")
    try:
        # print(f"Processing File: {path} ...", end="", flush=True)
        file_cache = ""
        with open(path, 'r') as file:
            file_cache = file.read()
#         history.append({"role": "user", "content": f"""Analyze Python class methods and provide the following for each:
# 1. `method_name(parameters)`:
#    - Parameters: param1 (type): description, param2 (type): description
#    - Return Type: return_type
#    - Methods used: method1(paramA), method2(paramB,paramC), method3()
#    - Docstring: Brief description of method's purpose.
#    - Key libraries or dependencies used.
# Use "None" for no parameters or returns. Avoid "etc." or similar vague terms. Be concise but informative. Focus on the most important aspects without generalizing. This is the file: \n{file_cache}"""})
        history.append({"role": "user", "content": f"""{doc_prompt} {file_cache}"""})
        completion = client.chat.completions.create(
            # model="TheBloke/phi-2k-GGUF",
            # model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
            # model="Qwen/Qwen2-0.5B-Instruct-GGUF",
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=history,
            temperature=0.7,
            stream=True,
        )

        new_message = {"role": "assistant", "content": ""}
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                new_message["content"] += chunk.choices[0].delta.content
        
        with open(file_output, 'a', encoding='utf-8') as file:
            file.write(f'FILE: {path}\n' + new_message["content"] + '\n---------------------------------\n')

        logging.info(" Processed")
        history = init_history[:]
        # logging.debug(f"History reset - {len(history)} messages in history")
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        errors.append(path)
        continue

logging.error(f"Total Errors: {len(errors)}")

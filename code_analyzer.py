import logging, os, traceback
from openai import OpenAI
from get_methods import get_methods, get_methods_with_code

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

file_output = 'output.txt'
# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

init_history = [
    {"role": "system", "content": "You are an AI programming assistant. Engage with the user to understand requirements."},
]

history = init_history

msg = ''

files_and_methods = get_methods('C:\\truveris\\projects\\sierra-mvp\\simulation-service', use_absolute_path=True)
logging.info(f"Found {len(files_and_methods.keys())} files")
errors = []

if not os.path.exists(file_output):
    with open(file_output, 'w') as file:
        pass

with open(file_output, 'r') as file:
    lines = file.readlines()

methods_with_code = get_methods_with_code(files_and_methods)
logging.info(f"Will process {len(methods_with_code.keys())} files")

for path in methods_with_code.keys():
    logging.info(f"Processing File: {path} ...")
    try:
        with open(file_output, 'a') as file:
            file.write(f'FILE: {path}\n\n')
        # print(f"Processing File: {path} ...", end="", flush=True)
        for method in methods_with_code[path]:
            method_name = method['name']
            file_cache = method['method_code']
            history.append({"role": "user", "content": f"""Analyze Python class methods and provide the following for each:
    1. `method_name(parameters)`:
    - Parameters: param1 (type): description, param2 (type): description
    - Return Type: return_type
    - Methods used: List ALL methods called within this method, including self methods and external function calls. Format as method1(paramA), method2(paramB,paramC), method3(). If no methods are used, state "None".
    - Docstring: Brief description of method's purpose.
    - Key libraries or dependencies used: List main libraries imported or used.
    Use "None" for no parameters or returns. Avoid "etc." or similar vague terms. Be specific and concise. Ensure you list ALL methods used, even if they are numerous. This is crucial for understanding the method's dependencies.
    Analyze this file: 
    {file_cache}"""})
            completion = client.chat.completions.create(
                # > Modifica aqui el modelo que uses con LM Studio
                model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
                # model="Qwen/Qwen2-0.5B-Instruct-GGUF",
                # model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
                messages=history,
                temperature=0.7,
                stream=True,
            )
            new_message = {"role": "assistant", "content": ""}
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    new_message["content"] += chunk.choices[0].delta.content
            
            with open(file_output, 'a') as file:
                file.write(f'METHOD: {method_name}\n' +new_message["content"] + '\n-+--------------------------------\n')
            history = init_history[:]
    except Exception as e:
        traceback.print_exc()
        logging.error(f"Error processing file: {e}")
        errors.append(path)
        continue

logging.error(f"Total Errors: {len(errors)}")

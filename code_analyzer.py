import logging, os
from openai import OpenAI
from get_methods import get_methods

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

file_output = 'output_2.txt'
# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

init_history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned, concise and short answers that are both correct and helpful."},
    {"role": "user", "content": "You'll help analizing the following code, and create bullets about it, at the end give a short summary about it"},
]

history = init_history

msg = ''

files_and_methods = get_methods('C:\\truveris\\projects\\sierra-mvp\\simulation-service', use_absolute_path=True)
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
        history.append({"role": "user", "content": f"Analize, and explain with bullets about the following code, at the end give a short summary about it, I'm interested in the methods and the overall of the file \n{file_cache}"})

        completion = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=history,
            temperature=0.7,
            stream=True,
        )

        new_message = {"role": "assistant", "content": ""}
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                new_message["content"] += chunk.choices[0].delta.content
        
        with open(file_output, 'a') as file:
            file.write(f'FILE: {path}\n' +new_message["content"] + '\n---------------------------------\n')

        logging.info(" Processed")
        history = init_history[:]
        logging.info(f"History reset - {len(history)} messages in history")
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        errors.append(path)
        continue

logging.info(f"Total Errors: {len(errors)}")
logging.info(" - - - - - - - - - - - - - - - -")
logging.info(" - - - - - - - - - - - - - - - -")
logging.info(" - - - - - - - - - - - - - - - -")
logging.info(" - - - - - - - - - - - - - - - -")
logging.info(" - - - - - - - - - - - - - - - -")
logging.info(" - - - - - - - - - - - - - - - -")
logging.info(" - - - - - - - - - - - - - - - -")
logging.info(" - - - - - - - - - - - - - - - -")
logging.info(" - - - - - - - - - - - - - - - -")
logging.info(" - - - - - - - - - - - - - - - -")

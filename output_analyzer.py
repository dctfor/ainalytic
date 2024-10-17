import logging
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

file_output = 'output.txt'
with open(file_output, 'r') as file:
    contents = file.read()
# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

init_history = [
    {"role": "system", "content": "You are an intelligent assistant that will give short answers that are both correct and helpful in a concise way."},
    # {"role": "user", "content": "You'll help analizing the text, and will try to join the pieces and tell how run the project"},
    # {"role": "user", "content": "You'll help analizing the text, and will try to join the pieces and tell what does"},
]

history = init_history

msg = ''
errors = []

logging.info(f"Processing File: {file_output} ...")
try:
    history.append({"role": "user", "content": f"""Given the following method, params and descriptions, provide:
1. A summary of the overall project purpose.
2. An explanation of how the methods work together.
3. Any key features or functionality of the project.
Be concise but comprehensive in your analysis. This is the file: \n{contents}"""})
#     history.append({"role": "user", "content": f"""Based on the code summary provided, create a concise project overview:
# 1. Project purpose (2-3 sentences)
# 2. How the main components work together (3-4 sentences)
# 3. Two key features or functionalities
# Limit your response to 150 words. Be specific and avoid vague terms like "etc." Focus on the most important aspects without generalizing. This is the file: \n{contents}"""})

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
    explained_file_output = f"{file_output}_explained.txt"
    with open(explained_file_output, 'w') as explained_file:
        explained_file.write(new_message["content"])
    logging.info("\nProcessed!\n---------------------------------")
except Exception as e:
    logging.error(f"Error processing file: {e}")

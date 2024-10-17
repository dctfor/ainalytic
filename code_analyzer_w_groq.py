import logging
# from openai import OpenAI
from get_methods import get_methods

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from groq import Groq
GROQ_API_KEY=['gsk_XXXYYYZZZAAABBCCDD','gsk_XXXYYYZZZAAABBCCDD']
client = Groq(
    api_key=GROQ_API_KEY[0],
    max_retries=1
)
client2 = Groq(
    api_key=GROQ_API_KEY[1],
    max_retries=1
)

init_history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned, concise and short answers that are both correct and helpful."},
    {"role": "user", "content": "You'll help analizing the following code, and create bullets about it, at the end give a short summary about it"},
]

history = init_history

msg = ''

files_and_methods = get_methods('./', use_absolute_path=False)

# while msg != 'q':
    # # Send the message to the API
    # completion = client.chat.completions.create(
    #     model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
    #     messages=history,
    #     temperature=0.7,
    #     stream=True,
    # )

    # # Create placeholder for the response
    # new_message = {"role": "assistant", "content": ""}
    
    # # Read the response from the API and place it in the placeholder
    # for chunk in completion:
    #     if chunk.choices[0].delta.content:
    #         print(chunk.choices[0].delta.content, end="", flush=True)
    #         new_message["content"] += chunk.choices[0].delta.content

    # history.append(new_message)
# files_and_methods = get_methods('C:\\truveris\\projects\\truguard-api-py\\', use_absolute_path=True)
files_and_methods = get_methods('.', use_absolute_path=True)

for path in files_and_methods.keys():
    logging.info(f"Processing File: {path} ...")
    # print(f"Processing File: {path} ...", end="", flush=True)
    file_cache = ""
    completion = None
    with open(path, 'r') as file:
        file_cache = file.read()
    history.append({"role": "user", "content": f"Analize, and explain with bullets about the following code, at the end give a short summary about it, I'm interested in the methods and the overall of the file \n{file_cache}"})

    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=history,
            timeout=5
        )
    except Exception as e:
        try:
            completion = client2.chat.completions.create(
                model="llama3-8b-8192",
                messages=history,
                timeout=5
            )
        except Exception as e:
            try:
                completion = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=history,
                    timeout=5
                )
            except Exception as e:
                completion = client2.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=history,
                    timeout=5
                )
            continue

    with open('output.txt', 'a') as file:
        file.write(f'FILE: {path}\n' + completion.choices[0].message.content + '\n---------------------------------\n')

    logging.info(" Processed")
    history = init_history

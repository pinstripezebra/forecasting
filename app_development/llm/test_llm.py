import os
from huggingface_hub import login, InferenceClient
from dotenv import find_dotenv, load_dotenv

# returning api key and logging in
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
key = os.getenv("HUGGING_FACE_API_KEY")
print(key)
login(key)

client = InferenceClient(model="meta-llama/Meta-Llama-3-70B-Instruct")

def llm_engine(messages, stop_sequences=["Task"]) -> str:
    response = client.chat_completion(messages, stop=stop_sequences, max_tokens=1000)
    answer = response.choices[0].message.content
    return answer

test_input = "what is the capital of france?"

print(llm_engine(test_input))
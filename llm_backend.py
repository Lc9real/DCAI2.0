from llama_cpp import Llama
from llm_memory import Memory_System
import os
from datetime import datetime



try:
    model_name = open("./Model/Model_Path.txt", "r").readlines()[0][4:]
except IndexError as e:
    raise IndexError("Model Path not Specified")
model_path = "C:/Users/lukac/SIA/Model/synthia-13b-v1.2.Q8_0.gguf"
if not os.path.exists(model_path):
    raise ValueError(f"Model does not exist check if the name is right")


temperature = 0.4
n_gpu_layer = 100
n_batch = 40
max_tokens = 6900
Debug = True

memory = Memory_System("SIA")

llm = Llama(
    model_path=model_path,
    temperature=temperature,
    n_gpu_layers=n_gpu_layer,
    n_batch=n_batch,
    max_tokens=max_tokens,
    top_p=1,
    n_ctx=max_tokens,
    verbose=False,
)


def call_Model(inp:str, channel_name:str, time, user_name="Unknown") -> str:
    user_timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    prompt = open("Prompt.txt", "r").read()
    input_prompt = prompt.format(user_name=user_name, input=inp, short_memory=memory.get_Memory(excluded_channel=str(channel_name)), timestamp=time, current_memory=memory.get_Memory(specific_channel=channel_name))
    if Debug:
        print(input_prompt)
    output = llm(input_prompt, max_tokens=20000, stop=[";"])
    llm_timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    if Debug:
        print(output["choices"][0]["text"])
    output["choices"][0]["text"] = "[hentai] {apple} @stormoutside"
    memory.add_Memory(user_name, inp, channel_name, user_timestamp)
    memory.add_Memory("SIA", output["choices"][0]["text"], channel_name, llm_timestamp)
    return output["choices"][0]["text"]
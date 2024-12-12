from modelscope import snapshot_download

model_dir = snapshot_download('LLM-Research/Meta-Llama-3-8B-Instruct', cache_dir='./620ccf/checkpoint')

model_dir = snapshot_download('AlexShu/ccf620', cache_dir='./620ccf/checkpoint')

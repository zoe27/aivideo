import os
import time
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


model = None
tokenizer = None

def load_model():
    global model, tokenizer
    if model is None or tokenizer is None:
        model_path = os.path.join(os.path.dirname(__file__), "m2m100-local")
        model = M2M100ForConditionalGeneration.from_pretrained(model_path)
        tokenizer = M2M100Tokenizer.from_pretrained(model_path)

load_model()

def translate_text(src_lang: str, tgt_lang: str, text: str) -> str:
    # # 加载本地模型
    # model_path = os.path.join(os.path.dirname(__file__), "m2m100-local")
    # # model_path = "./m2m100-local"
    # model = M2M100ForConditionalGeneration.from_pretrained(model_path)
    # tokenizer = M2M100Tokenizer.from_pretrained(model_path)

    # 设置源语言
    tokenizer.src_lang = src_lang

    # 预处理输入
    inputs = tokenizer(text, return_tensors="pt")

    # 生成翻译
    start_time = time.time()
    generated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.get_lang_id(tgt_lang))
    end_time = time.time()

    print(f"翻译耗时：{end_time - start_time:.2f} 秒")

    # 解码翻译结果
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translated_text

def translate_srt_file(input_file: str, output_file: str, src_lang: str, tgt_lang: str):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    translated_lines = []
    for line in lines:
        if line.strip() and not line.strip().isdigit() and '-->' not in line:
            translated_text = translate_text(src_lang, tgt_lang, line.strip())
            translated_lines.append(translated_text + '\n')
        else:
            translated_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(translated_lines)


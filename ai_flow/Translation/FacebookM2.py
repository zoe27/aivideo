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


import time

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# model_name = "facebook/m2m100_418M"  # 也可以换成 "facebook/m2m100_1.2B"
#
# # 下载并保存到本地
# model = M2M100ForConditionalGeneration.from_pretrained(model_name)
# tokenizer = M2M100Tokenizer.from_pretrained(model_name)
#
# model.save_pretrained("./m2m100-local")
# tokenizer.save_pretrained("./m2m100-local")


from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# 加载本地模型
model_path = "./m2m100-local"
model = M2M100ForConditionalGeneration.from_pretrained(model_path)
tokenizer = M2M100Tokenizer.from_pretrained(model_path)

# 设置语言（示例：英语翻译为中文）
tokenizer.src_lang = "en"

text = ("Hello, how are you, my name is ruoyizhou, and I am working on the AI, I want to "
        "create a tool that can work for the video trans")

# 预处理输入
inputs = tokenizer(text, return_tensors="pt")


# 生成翻译
start_time = time.time()
generated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.get_lang_id("zh"))
end_time = time.time()

print(f"翻译耗时：{end_time - start_time:.2f} 秒")

# 解码翻译结果
translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
print(translated_text)  # 输出: 你好，你好吗？


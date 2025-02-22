# 示例调用
from ai_flow.Translation.FacebookM2 import translate_text

src_lang = "en"
tgt_lang = "zh"
text = ("Hello, how are you, my name is ruoyizhou, and I am working on the AI, I want to "
        "create a tool that can work for the video trans")

translated_text = translate_text(src_lang, tgt_lang, text)
print(translated_text)  # 输出: 你好，你好吗？


translated_text_1 = translate_text(src_lang, "ja", text)
print(translated_text_1)  # 输出: 你好，你好吗？
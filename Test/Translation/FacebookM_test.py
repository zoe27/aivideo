# 示例调用
import os
import unittest

from ai_flow.Translation.FacebookM2 import translate_text, translate_srt_file


def test_translate_text(self):
    src_lang = "en"
    tgt_lang = "zh"
    text = ("Hello, how are you, my name is ruoyizhou, and I am working on the AI, I want to "
            "create a tool that can work for the video trans")

    translated_text = translate_text(src_lang, tgt_lang, text)
    print(translated_text)  # 输出: 你好，你好吗？

    translated_text_1 = translate_text(src_lang, "ja", text)
    print(translated_text_1)  # 输出: 你好，你好吗？

class TestTranslateSrtFile(unittest.TestCase):
    def setUp(self):
        self.input_file = 'test_input.srt'
        self.output_file = 'test_output.srt'
        self.src_lang = 'en'
        self.tgt_lang = 'zh'
        with open(self.input_file, 'w', encoding='utf-8') as f:
            f.write("1\n00:00:00,000 --> 00:00:02,000\nHello, how are you?\n")

    def tearDown(self):
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_translate_srt_file(self):
        translate_srt_file(self.input_file, self.output_file, self.src_lang, self.tgt_lang)
        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("你好,你怎么样", content)

if __name__ == '__main__':
    unittest.main()
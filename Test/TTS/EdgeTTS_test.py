import os
import unittest
import asyncio
import pysrt
from ai_flow.Text2Voice.EdgeTTS_srt import process_subtitles

class TestEdgeTTS(unittest.TestCase):
    def setUp(self):
        # 创建一个临时的 SRT 文件用于测试
        self.srt_file_path = 'test_subtitles.srt'
        with open(self.srt_file_path, 'w', encoding='utf-8') as file:
            file.write("""1
00:00:01,000 --> 00:00:04,000
Hello, this is a test.

2
00:00:05,000 --> 00:00:08,000
This is the second subtitle.
""")

    def tearDown(self):
        # 删除测试过程中生成���文件
        if os.path.exists(self.srt_file_path):
            os.remove(self.srt_file_path)
        if os.path.exists('final_output.mp3'):
            os.remove('final_output.mp3')
        for i in range(1, 3):
            audio_path = f'audio_{i}.mp3'
            if os.path.exists(audio_path):
                os.remove(audio_path)

    def test_process_subtitles(self):
        # 加载测试用的 SRT 文件
        subtitles = pysrt.open(self.srt_file_path)

        # 运行 process_subtitles 函数
        asyncio.run(process_subtitles(subtitles))

        # 检查生成的最终音频文件是否存在
        self.assertTrue(os.path.exists('final_output.mp3'))

if __name__ == '__main__':
    unittest.main()
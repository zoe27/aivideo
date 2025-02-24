import os
import unittest
from ai_flow.Voice2Text.WhisperSTT import transcribe_audio_to_srt


class TestWhisperTTS(unittest.TestCase):
    def test_transcribe_audio_to_srt(self):
        audio_file = "284abbe510e4697da7a2c7b11607767e.mp3"
        srt_output_path = "test_output.srt"

        result = transcribe_audio_to_srt(audio_file, srt_output_path)

        self.assertEqual(result, srt_output_path)
        # 检查生成的 SRT 文件是否存在
        self.assertTrue(os.path.exists(srt_output_path))

        # 读取 SRT 文件并检查内容是否合理
        with open(srt_output_path, 'r') as file:
            content = file.read()
            self.assertIn("1", content)  # 检查字幕编号
            self.assertIn("-->", content)  # 检查时间戳格式
            self.assertGreater(len(content), 0)  # 检查文件内容不为空

        # 删除生成的 SRT 文件
        os.remove(srt_output_path)


if __name__ == '__main__':
    unittest.main()

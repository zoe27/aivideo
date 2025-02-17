import asyncio
import os
import edge_tts

# seems this is the best solution right now

text = "大家好，我是zoe，一名对技术充满热情的软件开发者。我的主要技术栈包括 JavaScript、Python 和 Solidity，并且熟悉 Web3 相关技术，如智能 合约开发和去中心化应用（DApp）构建。我热衷于开源社区，曾在 GitHub 上参与过多个项目贡献。目前，我正在深入研究区块链技术，希望通过不断学习和实践，提高自己的能力。 我喜欢挑战新事物，并乐于解决复杂问题。如果有机会，我希望能与志同道合的朋友一起交流，共同探索技术的无限可能！) 期待与大家合作交流，谢谢！"

text = ("大家好，Web3 正在重新定义互联网的未来。它不仅仅是一个技术概念，"
        "更是一场关于去中心化、数据主权和信任的革命。与 Web2 时代不同，"
        "Web3 让用户真正拥有自己的数据，并通过区块链技术保障透明性和安全性。"
        "当前，我们看到去中心化金融（DeFi）、NFT、DAO 等创新应用蓬勃发展，"
        "但 Web3 仍处于早期阶段，面临着技术性能、用户体验和法规合规等挑战。"
        "未来，Layer 2 解决方案、零知识证明等技术将推动 Web3 走向更广泛的"
        "应用。对于开发者和用户来说，Web3 代表着新的机遇。它不仅可以创造更加开放、"
        "公平的互联网，也为个人和企业带来了前所未有的创新空间。让我们共同期待 Web3 时代的到来！")

voice = "zh-CN-XiaoyiNeural"  # 选择微软的中文女声
# voice = "zh-CN-shaanxi-XiaoniNeural"  # 选择微软的中文女声

async def main():
    tts = edge_tts.Communicate(text, voice)
    await tts.save("output.wav")  # 生成MP3文件
    print("语音已保存为 output.mp3")

asyncio.run(main())
os.system("afplay output.wav")  # macOS


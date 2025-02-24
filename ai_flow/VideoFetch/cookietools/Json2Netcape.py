import json
import time


def json_to_netscape(json_data):
    # 打开并格式化 cookies.txt 文件头
    netscape_header = "# Netscape HTTP Cookie File\n# This is a generated file!  Do not edit.\n\n"

    # 初始化转换后的内容
    netscape_cookies = []

    # 遍历 JSON 数据并提取 cookie 信息
    for cookie in json_data:
        domain = cookie.get('domain', '')
        path = cookie.get('path', '/')
        secure = 'TRUE' if cookie.get('secure', False) else 'FALSE'
        expiration = int(cookie.get('expirationDate', 0))
        name = cookie.get('name', '')
        value = cookie.get('value', '')

        # 将过期时间从 UNIX 时间戳转为格式化的字符串
        if expiration != 0:
            expiration_str = str(expiration)
        else:
            expiration_str = '0'  # 设置为 '0' 如果没有设置过期时间

        # 按照 Netscape 格式构建每个 cookie
        netscape_cookie = f"{domain}\tTRUE\t{path}\t{secure}\t{expiration_str}\t{name}\t{value}\n"
        netscape_cookies.append(netscape_cookie)

    # 合并 header 和 cookie 数据
    return netscape_header + ''.join(netscape_cookies)


def save_netscape_cookie(json_file, output_file):
    # 读取 JSON 文件
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    # 转换为 Netscape 格式
    netscape_cookies = json_to_netscape(json_data)

    # 保存到指定的输出文件
    with open(output_file, 'w') as f:
        f.write(netscape_cookies)

    print(f"Cookies have been saved to {output_file}")


# 示例用法
if __name__ == "__main__":
    # 输入的 JSON 文件路径
    json_file = 'exported-cookies.json'

    # 输出的 Netscape 格式文件路径
    output_file = 'cookies.txt'

    # 执行转换并保存
    save_netscape_cookie(json_file, output_file)

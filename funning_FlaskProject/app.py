from flask import Flask, render_template
import httpx
from datetime import datetime
import random

app = Flask(__name__)

# 搞笑表情符号集合
EMOJIS = ["😂", "🤣", "😆", "😅", "😄", "😁", "🤪", "😜", "🤩", "👻", "🤡", "🎭"]


@app.route('/')
def get_jokes():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {'key': '9e21081587f15c2cfdc19612c6d002cd'} #接口申请地址https://www.juhe.cn/docs/o1
    url = "http://v.juhe.cn/joke/randJoke"

    try:
        r = httpx.get(url, headers=headers, params=params)
        data = r.json()

        if data.get('error_code') == 0:
            # 转换时间戳并添加随机表情
            jokes = []
            for joke in data['result']:
                joke['time'] = datetime.fromtimestamp(joke['unixtime']).strftime('%Y-%m-%d %H:%M:%S')
                joke['emoji'] = random.choice(EMOJIS)
                jokes.append(joke)

            return render_template('jokes.html',
                                   jokes=jokes,
                                   page_emoji=random.choice(EMOJIS))
        else:
            return render_template('error.html',
                                   error=data.get('reason', '未知错误'),
                                   error_emoji=random.choice(EMOJIS))

    except Exception as e:
        return render_template('error.html',
                               error=str(e),
                               error_emoji=random.choice(["😱", "🤯", "😵"]))


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, Response
import httpx
import requests

app = Flask(__name__)

# 抖音API配置
DOUYIN_API = "http://101.35.2.25/api/fun/douyin.php"
API_PARAMS = {
    'id': '10005070',
    'key': '614871a88d4969af9d7f10b8077ffdd7'
}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return render_template('index.html', error="请输入抖音链接")

        try:
            params = API_PARAMS.copy()
            params['url'] = url

            with httpx.Client() as client:
                r = client.get(DOUYIN_API, params=params)
                data = r.json()

            if data.get('code') != 200:
                return render_template('index.html', error="解析失败，请检查链接是否正确")

            return render_template('index.html', data=data)

        except Exception as e:
            return render_template('index.html', error=f"解析出错: {str(e)}")

    return render_template('index.html')


@app.route('/proxy')
def proxy():
    """通用代理路由，处理图片和视频"""
    url = request.args.get('url')
    if not url:
        return "缺少URL参数", 400

    try:
        headers = {
            'Referer': 'https://www.douyin.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        req = requests.get(url, headers=headers, stream=True)
        return Response(
            req.iter_content(chunk_size=1024),
            content_type=req.headers['Content-Type'],
            headers={
                'Content-Disposition': 'inline'
            }
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
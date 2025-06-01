from flask import Flask, render_template
import httpx
from datetime import datetime

app = Flask(__name__)


def get_earthquake_data():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {'id': '10005070', 'key': '614871a88d4969af9d7f10b8077ffdd7'}
    url = "http://101.35.2.25/api/tianqi/dizhen.php"

    try:
        r = httpx.get(url, headers=headers, params=params)
        data = r.json()

        if data.get('code') == 200 and data.get('data'):
            earthquakes = []
            for quake in data['data']:
                magnitude = float(quake['leve'])

                if magnitude >= 7.0:
                    level = "重大地震"
                    css_class = "major"
                elif magnitude >= 6.0:
                    level = "强震"
                    css_class = "strong"
                elif magnitude >= 5.0:
                    level = "中强震"
                    css_class = "moderate"
                elif magnitude >= 4.0:
                    level = "轻震"
                    css_class = "light"
                else:
                    level = "微震"
                    css_class = "minor"

                earthquakes.append({
                    'magnitude': quake['leve'],
                    'time': quake['addtime'],
                    'location': quake['weizhi'],
                    'latitude': quake['weidu'],
                    'longitude': quake['jingdu'],
                    'depth': quake['shendu'],
                    'level': level,
                    'css_class': css_class,
                    'details_url': quake['tourl']
                })

            return {
                'success': True,
                'count': len(earthquakes),
                'earthquakes': earthquakes
            }
        else:
            return {
                'success': False,
                'message': data.get('message', '未知错误'),
                'code': data.get('code', '无')
            }
    except Exception as e:
        return {
            'success': False,
            'message': f"请求失败: {str(e)}"
        }


@app.route('/')
def index():
    data = get_earthquake_data()
    return render_template('index.html', data=data, now=datetime.now())


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
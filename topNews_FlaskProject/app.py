from flask import Flask, render_template, request
import httpx

app = Flask(__name__)

# 新闻类型映射
NEWS_TYPES = {
    'top': '推荐',
    'guonei': '国内',
    'guoji': '国际',
    'yule': '娱乐',
    'tiyu': '体育',
    'junshi': '军事',
    'keji': '科技',
    'caijing': '财经',
    'youxi': '游戏',
    'qiche': '汽车',
    'jiankang': '健康'
}


@app.route('/')
def index():
    # 默认显示推荐新闻
    return news_list('top', 1)


@app.route('/news/<news_type>/<int:page>')
def news_list(news_type, page):
    # 验证新闻类型
    if news_type not in NEWS_TYPES:
        return render_template('error.html', error="无效的新闻类型")

    # 验证页码
    if page < 1 or page > 50:
        return render_template('error.html', error="页码必须在1-50之间")

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {
        'key': '',##接口申请地址https://www.juhe.cn/docs/api/id/235
        'type': news_type,
        'page': page,
        'is_filter':1,
        'page_size': 30  # 每页10条
    }

    try:
        r = httpx.get("http://v.juhe.cn/toutiao/index", headers=headers, params=params)
        data = r.json()

        if data.get('error_code') == 0 and data.get('result', {}).get('stat') == '1':
            news_list = data['result']['data']
            total = len(news_list)

            return render_template('news.html',
                                   news_list=news_list,
                                   news_type=news_type,
                                   current_page=page,
                                   news_types=NEWS_TYPES,
                                   type_name=NEWS_TYPES[news_type])
        else:
            return render_template('error.html', error=data.get('reason', '未知错误'))

    except Exception as e:
        return render_template('error.html', error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
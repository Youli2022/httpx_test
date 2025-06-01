from flask import Flask, render_template, request
import httpx

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone = request.form.get('phone')

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {'phone': phone, 'key': 'ceb0d0562ffaab815d7464860b0f3f29'} #接口申请地址https://www.juhe.cn/docs/o1
        url = "http://apis.juhe.cn/mobile/get"

        try:
            r = httpx.get(url, headers=headers, params=params)
            data = r.json()

            if data['resultcode'] == '200' and data['error_code'] == 0:
                result = data['result']
                return render_template('result.html',
                                       phone=phone,
                                       province=result['province'],
                                       city=result['city'],
                                       company=result['company'],
                                       areacode=result['areacode'],
                                       zip_code=result['zip'])
            else:
                if data['reason'] == 'Wrong phone number!':
                    error = "请输入正确的手机号！"
                else:
                    error = data['reason']
                return render_template('index.html', error=error)

        except Exception as e:
            return render_template('index.html', error=f"查询出错: {str(e)}")

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
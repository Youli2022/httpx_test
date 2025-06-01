from flask import Flask, render_template, request, jsonify
import httpx

app = Flask(__name__)

# QQ靓号分类信息
QQ_NUMBER_TYPES = {
    "按位数分类": {
        "5位号": "非常稀有，市场价值高",
        "6位号": "较为稀有，价值较高",
        "7位号": "相对常见，价值中等",
        "8位号": "普通号码，价值一般",
        "9位号": "新号段，价值较低",
        "10位号": "最新号段，价值最低"
    },
    "按数字特性分类": {
        "全A号": "如666666、888888等重复数字",
        "AB号": "如121212、343434等交替数字",
        "ABC号": "如123123、456456等循环数字",
        "回旋号": "如12321、45654等对称数字",
        "重叠号": "如112233、445566等成对数字",
        "顺子号": "如123456、56789等连续数字",
        "豹子号": "如111111、222222等相同数字"
    },
    "按概念意义分类": {
        "生日号": "如19900101、19881212等生日日期",
        "手机号": "与手机号码相同的QQ号",
        "客服号": "如80000、10000等类似客服号码",
        "区号": "如010、021等城市区号",
        "年份号": "如2008、2020等年份数字"
    }
}


@app.route('/')
def index():
    return render_template('index.html', qq_types=QQ_NUMBER_TYPES)


@app.route('/query', methods=['POST'])
def query_qq():
    qq = request.form.get('qq')

    if not qq or not qq.isdigit():
        return jsonify({"error": "请输入有效的QQ号码"}), 400

    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {
            'id': '10005070',
            'key': '614871a88d4969af9d7f10b8077ffdd7',
            'qq': qq,
            'ckqq': '1456813619',
            'skey': '@iEfYUG4Tl',
            'pskey': 'dNeSR6-vzKtO6pp1WZgr*6Y4ZuC9SIEFh6AAnFQzrP4_',
        }
        url = "http://101.35.2.25/api/other/qq.php"

        r = httpx.get(url, headers=headers, params=params)
        data = r.json()

        if data.get('code') == 200:
            # 添加估价逻辑
            data['valuation'] = estimate_qq_value(qq, data)  # 第二个参数传入data
            return render_template('result.html', data=data)
        else:
            return render_template('result.html', error=f"查询失败，错误码: {data.get('code')}")

    except httpx.RequestError as e:
        return render_template('result.html', error=f"网络请求失败: {str(e)}")
    except ValueError as e:
        return render_template('result.html', error="返回数据解析失败")
    except Exception as e:
        return render_template('result.html', error=f"发生错误: {str(e)}")


def estimate_qq_value(qq,data):
    """文化寓意综合估价逻辑"""
    total = 0

    # 一、数字组合与寓意价值
    # 1. 九五之尊映射（按出现次数计算）
    total += qq.count('5') * 100  # 每个5加100元
    total += qq.count('8') * 100  # 每个8加100元

    # 2. 数字情绪性价值（按存在性计算）
    emotion_values = {
        '0': 150,  # 圆满宁静
        '1': 150,  # 独立新生
        '2': 150,  # 平衡和谐
        '3': 200,  # 完整发展
        '5': 250,  # 尊贵权威
        '7': 200,  # 生机活力
        '8': 300  # 财富繁荣
    }
    unique_digits = set(qq)
    for d in emotion_values:
        if d in unique_digits:
            total += emotion_values[d]

    # 3. 组合流畅度加成
    total += 200  # 流畅度及独特性

    # 二、等级与天数价值
    # 1. 等级价值（线性计算）
    level = int(data.get('Level', 0))
    total += max(level * 15, 0)  # 每级15元

    # 2. 等级天数价值（指数计算）
    network_days = int(data.get('NetworkDay', 0))
    total += int(network_days ** 0.7)  # 8319天≈800元

    # 3. 距下级天数价值
    next_days = int(data.get('Next', 0))
    total += min(next_days * 2, 300)  # 每天2元，上限300

    # 三、状态价值
    # 1. 会员纯净价值
    if data.get('iVip') != '1':
        total += 100  # 非会员纯净加成

    # 2. PC状态价值
    if data.get('iPCQQOnline') != '1':
        total += 50  # 离线沉淀价值

    # 3. 成长天数价值
    base_days = float(data.get('iBaseDays', 0))
    if base_days == 0:
        total += 100  # 新起点潜力值

    # 四、生成估价范围
    base_value = total
    fluctuation = int(base_value * 0.3)  # 30%波动范围
    return f"{base_value - fluctuation}-{base_value + fluctuation}元"

def is_repeating(qq):
    """检查是否是豹子号"""
    return len(set(qq)) == 1


def is_sequential(qq):
    """检查是否是顺子号"""
    return all(int(qq[i]) + 1 == int(qq[i + 1]) for i in range(len(qq) - 1)) or \
        all(int(qq[i]) - 1 == int(qq[i + 1]) for i in range(len(qq) - 1))


def is_symmetric(qq):
    """检查是否是对称号"""
    return qq == qq[::-1]


def is_pair(qq):
    """检查是否是重叠号"""
    if len(qq) % 2 != 0:
        return False
    for i in range(0, len(qq), 2):
        if qq[i] != qq[i + 1]:
            return False
    return True


if __name__ == '__main__':
    app.run(debug=True)
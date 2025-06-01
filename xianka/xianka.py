import httpx


def fetch_xianka_ranking():
    url = "https://cn.apihz.cn/api/bang/xianka1.php"
    params = {
        'id': '10005070',
        'key': '614871a88d4969af9d7f10b8077ffdd7'
    }

    try:
        # 发送GET请求
        response = httpx.get(url, params=params)
        response.raise_for_status()  # 检查HTTP状态码是否异常

        data = response.json()

        # 检查返回码
        if data.get('code') != 200:
            print(f"请求失败，错误码：{data.get('code')}")
            return

        # 解析数据
        time_str = data.get('time2', '未知时间')
        ranking_data = data.get('data', [])

        print(f"显卡天梯榜（更新时间：{time_str}）\n")
        for item in ranking_data:
            print(f"TOP {item['top']}: {item['name']}")

    except httpx.RequestError as e:
        print(f"网络请求失败：{str(e)}")
    except ValueError:
        print("返回数据解析失败，可能不是有效的JSON格式")
    except KeyError as e:
        print(f"返回数据缺少必要字段：{str(e)}")


if __name__ == "__main__":
    fetch_xianka_ranking()
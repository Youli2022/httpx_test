import httpx

headers = {"Content-Type": "application/x-www-form-urlencoded"}
params = {'id': '10005070', 'key': '614871a88d4969af9d7f10b8077ffdd7', }
url = "http://101.35.2.25/api/tianqi/dizhen.php"
r = httpx.get(url, headers=headers, params=params)
data = r.json()
print(data)

if data.get('code') == 200 and data.get('data'):
    earthquake_list = data['data']

    print(f"共获取 {len(earthquake_list)} 条地震数据：\n")

    for i, quake in enumerate(earthquake_list, 1):
        print(f"{i}. 震级: {quake['leve']}级")
        print(f"   时间: {quake['addtime']}")
        print(f"   位置: {quake['weizhi']}")
        print(f"   坐标: 纬度 {quake['weidu']}, 经度 {quake['jingdu']}")
        print(f"   深度: {quake['shendu']}公里")

        # 根据震级添加地震等级描述
        magnitude = float(quake['leve'])
        if magnitude >= 7.0:
            level = "重大地震"
        elif magnitude >= 6.0:
            level = "强震"
        elif magnitude >= 5.0:
            level = "中强震"
        elif magnitude >= 4.0:
            level = "轻震"
        else:
            level = "微震"
        print(f"   等级: {level}")

        print(f"   详情链接: {quake['tourl']}\n")

else:
    print(f"请求失败: {data.get('message', '未知错误')} (错误码: {data.get('code', '无')})")

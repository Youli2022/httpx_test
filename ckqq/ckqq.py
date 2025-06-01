import httpx

qq = input(f"请输入您的QQ号：")
headers = {"Content-Type": "application/x-www-form-urlencoded"}
params = {'id': '10005070',
          'key': '614871a88d4969af9d7f10b8077ffdd7',
          'qq': qq,
          'ckqq': '1456813619',
          'skey': '@iEfYUG4Tl',
          'pskey': 'dNeSR6-vzKtO6pp1WZgr*6Y4ZuC9SIEFh6AAnFQzrP4_', }
url = "http://101.35.2.25/api/other/qq.php"
r = httpx.get(url, headers=headers, params=params)

data = r.json()
print(data)

try:
    r = httpx.get(url, headers=headers, params=params)
    data = r.json()

    if data['code'] == 200:
        brief_info = f"QQ号: {data['qq']}\n" \
                     f"昵称: {data['Name']}\n" \
                     f"头像: {data['head']}\n" \
                     f"QQ等级: {data['Level']} ({data['Icon']})\n" \
                     f"等级天数: {data['NetworkDay']} (距下级还需{data['Next']}天)\n" \
                     f"会员状态: {'VIP' + data['iVipLevel'] if data['iVip'] == '1' else '非会员'}" \
                     f"{'(超级会员)' if data['iSVip'] == '1' else ''}" \
                     f"{'(年费会员)' if data['iYearVip'] == '1' else ''}\n" \
                     f"PC状态: {'在线' if data['iPCQQOnline'] == '1' else '离线'}\n" \
                     f"成长天数: {data['TheDays']}天 (基础:{data['iBaseDays']}天)"
        print(brief_info)
    else:
        print(f"查询失败，错误码: {data['code']}")

except httpx.RequestError as e:
    print(f"网络请求失败: {str(e)}")
except ValueError as e:
    print("返回数据解析失败")
except KeyError as e:
    print(f"返回数据缺少必要字段: {str(e)}")

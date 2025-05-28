import httpx

phone = input(f"请输入您的手机号：")
headers = {"Content-Type": "application/x-www-form-urlencoded"}
params = {'phone': phone, 'key': ''}  ##接口申请地址:https://www.juhe.cn/docs/api/id/11
url = "http://apis.juhe.cn/mobile/get"
r = httpx.get(url, headers=headers, params=params)

data = r.json()
print(data)
if data['resultcode'] == '200' and data['error_code'] == 0:
    result = data['result']

    brief_info = f"手机号: {params['phone']}\n" \
                 f"归属地: {result['province']}省 {result['city']}市\n" \
                 f"运营商: {result['company']}\n" \
                 f"区号: {result['areacode']}\n" \
                 f"邮编: {result['zip']}"
    print(brief_info)
else:
    if data['reason'] == 'Wrong phone number!':
        print(f"查询失败，请输入正确的手机号！")
    else:
        print(f"查询失败，原因: {data['reason']}")

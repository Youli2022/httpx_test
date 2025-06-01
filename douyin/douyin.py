import httpx

url = input(f"请输入抖音链接：")
headers = {"Content-Type": "application/x-www-form-urlencoded"}
params = {'id':'10005070', 'key': '614871a88d4969af9d7f10b8077ffdd7','url':url}  #接口申请地址:https://www.apihz.cn/api/fundouyin.html
url = "http://101.35.2.25/api/fun/douyin.php"
r = httpx.get(url, headers=headers, params=params)

data = r.json()
print(data)